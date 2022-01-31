import os
import csv
import random
import sys, getopt

# from modules.redmine_connection import *
from modules.jira_connection import *
from modules.outlook_connection import *
from modules.common import *

from datetime import datetime, timedelta
from tzlocal import get_localzone

import warnings
from pprint import pprint


SECONDS_IN_HOUR = 3600
SETTINGS_FILE = 'settings.json'


def write_from_calendar(config, start_time, end_time):
    categories = config.categories

    black_list = []
    jira_connection = Jira_Connection(сonfig.jira, сonfig.login, сonfig.password)
    # TODO: When we use redmine...
    # redmine_connection = Redmine_Connection(сonfig.redmine, сonfig.login, сonfig.password)

    meetings = read_outlook(config, start_time, end_time)

    for calendar_item in meetings:
        difference = calendar_item.end - calendar_item.start
        meeting = Meeting(calendar_item.subject, calendar_item.start, difference.seconds / SECONDS_IN_HOUR)

        if (calendar_item.categories is None):
            category = categories[None]
        else:

            if (config.ignore in calendar_item.categories):
                black_list.append(meeting)
                continue

            if (calendar_item.categories[0] not in categories):
                category = categories[None]
            else:
                category = categories[calendar_item.categories[0]]

        category.add_meeting(meeting)

    save_file(black_list)

    for category_name in categories:
        category = categories[category_name]
        jira_connection.write_meeting(category.jira_issue_id, category.meetings)
        # TODO: When we use redmine...
        # redmine_connection.write_meeting(category.redmine_issue_id, category.meetings)


def save_file(meetings):
    with open('black_list', 'a', encoding='utf8') as file:
        file.write('-----------{} at {}\n'.format("Black list", datetime.now().strftime("%y-%m-%d")))

        for meeting in meetings:
            file.write('{}, {}, {}\n'.format(meeting.name, meeting.date, meeting.duration))

        file.write('\n')


def periodical(сonfig, start_time, end_time):

    date_generated = [start_time + timedelta(days=x) for x in range(0, (end_time-start_time).days)]
    hours = 0.5

    jira_connection = Jira_Connection(сonfig.jira, сonfig.login, сonfig.password)
    # TODO: When we use redmine...
    # redmine_connection = Redmine_Connection(сonfig.redmine, сonfig.login, сonfig.password)

    for date in date_generated:
        weekno = date.weekday()
        if weekno > 4: # 4 is Friday
            continue
            
        for task in сonfig.periodical:
            meeting = Meeting(task.name, date, hours)
            task.add_meeting(meeting)

    for task in сonfig.periodical:
        jira_connection.write_meeting(task.jira_issue_id, task.meetings)
        # TODO: When we use redmine...
        # redmine_connection.write_meeting(category.redmine_issue_id, category.meetings)


def read_outlook(config, start_time, end_time):
    domain_login = f'{config.domain}\\{config.login}'
    outlook_connection = Outlook_Connection(config.outlook, config.email, domain_login, сonfig.password)
    return outlook_connection.get_meeting(start_time, end_time)


def convert_rawdate_to_datetime(raw_date):
    # convert from string format to datetime format
    return datetime.strptime(raw_date, '%Y/%m/%d')


def read_tasks(config, start_time, end_time):
    domain_login = '{}\\{}'.format(config.domain, config.login)
    outlook_connection = Outlook_Connection(config.outlook, config.email, domain_login, сonfig.password)
    return outlook_connection.get_tasks(start_time, end_time)


def get_hours_by_date(config, start_time):
    jira_connection = Jira_Connection(сonfig.jira, сonfig.login, сonfig.password)
     # Получаем issues, по которым было списано время за дату, по которой собирается KPI
    nextDay = start_time + timedelta(days=1)
    issues = jira_connection.jira.search_issues(f'worklogAuthor = "{сonfig.login}" AND worklogDate >= "{start_time.strftime("%Y/%m/%d")}" AND worklogDate < "{nextDay.strftime("%Y/%m/%d")}"')

    # Собираем worklog-и, которые были и созданы и списаны в дату, по которой собирается KPI
    worklogs = []
    for issue in issues:
        issueWorklogs = jira_connection.jira.worklogs(issue.key)

        # Используется strptime т.к. datetime.fromisoformat не может распарсить часовой пояса без двоиточия
        filtredIssueWorklogs = list(filter(lambda o: o.author.name == сonfig.login
            and datetime.strptime(o.started, '%Y-%m-%dT%H:%M:%S.%f%z').date() >= start_time.date() 
            and datetime.strptime(o.started, '%Y-%m-%dT%H:%M:%S.%f%z').date() < nextDay.date()
            , issueWorklogs))

        if len(filtredIssueWorklogs) > 0:
            worklogs.extend(filtredIssueWorklogs)
        
    if len(worklogs) == 0:
        return 0
    
    sum_timespent = 0
    for wl in worklogs:
        sum_timespent += wl.timeSpentSeconds
    
    return sum_timespent / SECONDS_IN_HOUR


def create_sub_issue(config, task_categories, name):
    if (task_categories is None):
        category = config.categories[None]
    else:
        if (task_categories[0] not in config.categories):
            category = config.categories[None]
        else:
            category = config.categories[task_categories[0]]

    parrent_issue_id = category.jira_issue_id

    jira_connection = Jira_Connection(сonfig.jira, сonfig.login, сonfig.password)
    new_issue = jira_connection.create_subtask(name, parrent_issue_id)
    return new_issue.key


def add_meeting_to_correct_category(config, name, jira_issue_id, date, diff):

    category = None

    if jira_issue_id not in config.categories:
        config.categories[jira_issue_id] = TasksCategory(name, jira_issue_id, None)
        category = config.categories[jira_issue_id]
    else:
        category = config.categories[jira_issue_id]

    jira_worklog = Meeting(name, date, diff)
    category.add_meeting(jira_worklog)


def get_correct_task(config, tasks, current_date, current_time):
    tasks_without_time = []

    selected_task = None
    for task_item in tasks:
        # print(f'\nTask: {task_item.subject}')
        # print(f'start_time: {task_item.start_date}')
        # print(f'current_time: {current_date} ')
        if task_item.start_date > current_date.date():
            # print(f'{task_item.subject} is not today.')
            continue

        if not 'all=' in task_item.subject:
            tasks_without_time.append(task_item)
            continue

        # print(f'{task_item.subject} is selected.')
        subtest = task_item.subject.split(';')
        if len(subtest) < 2:
            tasks_without_time.append(task_item)
            continue

        all_time = 0
        write_time = 0
        is_task_without_time = False
        raw_jira_issue_id = None
        for item in subtest:
            if 'all=' in item:
                raw_all_time = item.replace('all=', '')
                # print(f'raw_all_time: {raw_all_time}')
                if raw_all_time.isspace():
                    is_task_without_time = True
                else:
                    all_time = float(raw_all_time)
                
            if 'write=' in item:
                raw_write_time = item.replace('write=', '')
                # print(f'raw_write_time: {raw_write_time}')
                if not raw_write_time.isspace():
                    write_time = float(raw_write_time)
            if 'jira_issue_id=' in item:
                raw_jira_issue_id = item.replace('jira_issue_id=', '')

        if is_task_without_time:
            tasks_without_time.append(task_item)
            continue

        if write_time == all_time:
            tasks.remove(task_item)
            task_item.complete()
            task_item.save()
            # print(f'All time was writed: {subtest}')
            continue

        # print(f'All time was not writed: {subtest}')
        if all_time + current_time > 8.0:
            write_time = 8.0 - current_time
        else:
            write_time += all_time

        if raw_jira_issue_id == None or raw_jira_issue_id.isspace():
            jira_issue_id = create_sub_issue(config, task_item.categories, subtest[0])
        else:
            jira_issue_id = raw_jira_issue_id

        add_meeting_to_correct_category(config, subtest[0], jira_issue_id, current_date, write_time)
        task_item.subject = f'{subtest[0]}; all={all_time}; write={write_time}; jira_issue_id={jira_issue_id}'
        task_item.save()

        return task_item, write_time

    if len(tasks_without_time) != 0:
        write_time = 8 - current_time
        task_item = random.choice(tasks_without_time)
        subtest = task_item.subject.split(';')

        writed_time = 0
        raw_jira_issue_id = None
        for item in subtest:
            if 'write=' in item:
                raw_write_time = item.replace('write=', '')
                # print(f'raw_write_time: {raw_write_time}')
                if not raw_write_time.isspace():
                    writed_time = float(raw_write_time)
            if 'jira_issue_id=' in item:
                raw_jira_issue_id = item.replace('jira_issue_id=', '')
        
        if raw_jira_issue_id == None or raw_jira_issue_id.isspace():
            jira_issue_id = create_sub_issue(config, task_item.categories, subtest[0])
        else:
            jira_issue_id = raw_jira_issue_id

        add_meeting_to_correct_category(config, subtest[0], jira_issue_id, current_date, write_time)
        task_item.subject = f'{subtest[0]}; write={writed_time + write_time}; jira_issue_id={jira_issue_id}'
        task_item.save()
        return task_item, write_time
    return None, 0


def write_from_tasks(config, start_time, end_time):
    categories = config.categories
    black_list = []

    tasks = read_tasks(config, start_time, end_time)
    if len(tasks) == 0:
        print('Not tasks')
        return

    date_generated = [start_time + timedelta(days=x) for x in range(0, (end_time-start_time).days)]
    for date in date_generated:
        weekno = date.weekday()
        if weekno > 4: # 4 is Friday
            continue

        hours_by_date = get_hours_by_date(config, date)
        # print(hours_by_date)
        while hours_by_date < 8:
            # print(f'Before selected to {date}: Time {hours_by_date}')
            task, diff = get_correct_task(config, tasks, date, hours_by_date)

            if task is None:
                break

            hours_by_date += diff
            # print(f'Selected to {date}: Time {hours_by_date}; {task.subject}.')

    save_file(black_list)

    jira_connection = Jira_Connection(сonfig.jira, сonfig.login, сonfig.password)
    for category_name in categories:
        category = categories[category_name]
        jira_connection.write_meeting(category.jira_issue_id, category.meetings)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    try:
        arguments, values = getopt.getopt(sys.argv[1:], "hi:o:", ["start_time=", "end_time="])
    except getopt.GetoptError:
        print('meetings.py --start_time <start_time> --end_time <end_time>')
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s", "--start_time"):
            # print ('start_time = {}'.format(currentValue))
            start_time = convert_rawdate_to_datetime(currentValue)
             
        elif currentArgument in ("-e", "--end_time"):
            # print ('end_time = {}'.format(currentValue))
            end_time = convert_rawdate_to_datetime(currentValue)

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        сonfig = Config(raw_data)

    local_tz = get_localzone()
    start_time = start_time.replace(tzinfo=local_tz)
    end_time = end_time.replace(tzinfo=local_tz)

    сonfig.clear_categories()
    # write_from_calendar(сonfig, start_time, end_time)

    сonfig.clear_categories()
    # periodical(сonfig, start_time, end_time)

    сonfig.clear_categories()
    write_from_tasks(сonfig, start_time, end_time)