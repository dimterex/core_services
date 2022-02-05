from datetime import timedelta, datetime
import random

from modules.common.TaskCatogory import TasksCategory
from modules.common.Worklog import Worklog
from modules.helper import supported_day, SECONDS_IN_HOUR


class Worklog_By_Tasks:
    def __init__(self, configuration, start_time, end_time, issue_tracker, outlook, worklogs_service):
        self.worklogs_service = worklogs_service
        self.configuration = configuration
        self.start_time = start_time
        self.end_time = end_time
        self.issue_tracker = issue_tracker
        self.outlook = outlook

    def modify(self):
        return
        date_generated = [self.start_time + timedelta(days=x) for x in
                          range(0, (self.end_time - self.start_time).days)]
        hours = 0.5

        for date in date_generated:
            if not supported_day(date):
                continue

            for task in self.configuration.periodical:
                if task not in self.configuration.categories:
                    self.configuration.categories[task] = TasksCategory(task.name, task.jira_issue_id)

                category = self.configuration.categories[task]
                self.worklogs_service.add_worklog(Worklog(task.name, date, category.jira_issue_id, hours))


    def write_from_tasks(self, start_time, end_time):
        categories = self.configuration.categories

        tasks = self.outlook.get_tasks(start_time, end_time)
        if len(tasks) == 0:
            print('Not tasks')
            return

        date_generated = [start_time + timedelta(days=x) for x in range(0, (end_time - start_time).days)]
        for date in date_generated:
            if not supported_day(date):
                continue

            hours_by_date = self.get_hours_by_date(self.configuration, date)
            # print(hours_by_date)
            while hours_by_date < 8:
                # print(f'Before selected to {date}: Time {hours_by_date}')
                task, diff = self.get_correct_task(self.configuration, tasks, date, hours_by_date)

                if task is None:
                    break

                hours_by_date += diff
                # print(f'Selected to {date}: Time {hours_by_date}; {task.subject}.')

        # save_file(black_list)

        for category_name in categories:
            category = categories[category_name]
            self.issue_tracker.write_meeting(category.jira_issue_id, category.meetings)

    def get_hours_by_date(self, start_time):
        # Получаем issues, по которым было списано время за дату, по которой собирается KPI
        nextDay = start_time + timedelta(days=1)
        issues = self.issue_tracker.jira.search_issues(
            f'worklogAuthor = "{self.configuration.login}" AND worklogDate >= "{start_time.strftime("%Y/%m/%d")}" AND worklogDate < "{nextDay.strftime("%Y/%m/%d")}"')

        # Собираем worklog-и, которые были и созданы и списаны в дату, по которой собирается KPI
        worklogs = []
        for issue in issues:
            issueWorklogs = self.issue_tracker.jira.worklogs(issue.key)

            # Используется strptime т.к. datetime.fromisoformat не может распарсить часовой пояса без двоиточия
            filtredIssueWorklogs = list(filter(lambda o: o.author.name == self.configuration.login
                                                         and datetime.strptime(o.started,
                                                                               '%Y-%m-%dT%H:%M:%S.%f%z').date() >= start_time.date()
                                                         and datetime.strptime(o.started,
                                                                               '%Y-%m-%dT%H:%M:%S.%f%z').date() < nextDay.date()
                                               , issueWorklogs))

            if len(filtredIssueWorklogs) > 0:
                worklogs.extend(filtredIssueWorklogs)

        if len(worklogs) == 0:
            return 0

        sum_timespent = 0
        for wl in worklogs:
            sum_timespent += wl.timeSpentSeconds

        return sum_timespent / SECONDS_IN_HOUR

    def create_sub_issue(self, task_categories, name):
        if (task_categories is None):
            category = self.configuration.categories[None]
        else:
            if (task_categories[0] not in self.configuration.categories):
                category = self.configuration.categories[None]
            else:
                category = self.configuration.categories[task_categories[0]]

        parrent_issue_id = category.jira_issue_id

        new_issue = self.issue_tracker.create_subtask(name, parrent_issue_id)
        return new_issue.key

    def add_meeting_to_correct_category(self, name, jira_issue_id, date, diff):

        category = None

        if jira_issue_id not in self.configuration.categories:
            self.configuration.categories[jira_issue_id] = TasksCategory(name, jira_issue_id, None)
            category = self.configuration.categories[jira_issue_id]
        else:
            category = self.configuration.categories[jira_issue_id]

        jira_worklog = Worklog(name, date, category.jira_issue_id, diff)
        category.add_meeting(jira_worklog)

    def get_correct_task(self, tasks, current_date, current_time):
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
                # print(item)
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
                    # print(f'raw_jira_issue_id: {raw_jira_issue_id}')

            if is_task_without_time:
                tasks_without_time.append(task_item)
                continue

            if write_time >= all_time:
                tasks.remove(task_item)
                task_item.complete()
                task_item.save()
                print(f'All time was writed: {subtest}')
                continue

            # print(f'All time was not writed: {subtest}')
            if all_time + current_time > 8.0:
                write_time = 8.0 - current_time
            else:
                write_time += all_time

            if raw_jira_issue_id == None or raw_jira_issue_id.isspace():
                jira_issue_id = self.create_sub_issue(self, task_item.categories, subtest[0])
            else:
                jira_issue_id = raw_jira_issue_id

            self.add_meeting_to_correct_category(subtest[0], jira_issue_id, current_date, write_time)
            task_item.subject = f'{subtest[0]};all={all_time};write={write_time};jira_issue_id={jira_issue_id};'
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
                jira_issue_id = self.create_sub_issue(task_item.categories, subtest[0])
            else:
                jira_issue_id = raw_jira_issue_id

            self.add_meeting_to_correct_category(subtest[0], jira_issue_id, current_date, write_time)
            task_item.subject = f'{subtest[0]};write={writed_time + write_time};jira_issue_id={jira_issue_id};'
            task_item.save()
            return task_item, write_time
        return None, 0
