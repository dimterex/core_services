import os
import csv

from modules.redmine_connection import *
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
    jira_connection = Jira_Connection(сonfig.jira.url, сonfig.login, сonfig.password)
    # TODO: When we use redmine...
    # redmine_connection = Redmine_Connection(сonfig.redmine.url, сonfig.login, сonfig.password)

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

    jira_connection = Jira_Connection(сonfig.jira.url, сonfig.login, сonfig.password)
    # TODO: When we use redmine...
    # redmine_connection = Redmine_Connection(сonfig.redmine.url, сonfig.login, сonfig.password)

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
    domain_login = '{}\\{}'.format(config.domain, config.login)
    outlook_connection = Outlook_Connection(config.outlook.url, config.email, domain_login, сonfig.password)
    return outlook_connection.get_meeting(start_time, end_time)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        сonfig = Config(raw_data)


    local_tz = get_localzone()
    # TODO: set time from arguments
    start_time = datetime(2021, 10, 6, tzinfo=local_tz)
    end_time = datetime(2021, 10, 13, tzinfo=local_tz)

    # TODO: choose a method from arguments
    write_from_calendar(сonfig, start_time, end_time)
    periodical(сonfig, start_time, end_time)