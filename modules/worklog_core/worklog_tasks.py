from datetime import timedelta, datetime
import random

from modules.connections.jira_connection import Jira_Connection
from modules.connections.outlook_connection import Outlook_Connection
from modules.models.configuration import Configuration
from modules.models.outlook_task import Outlook_Task
from modules.worklog_core.helper import supported_day, NEEDS_HOURS
from modules.worklog_core.services.worklog_service import Worklog_Service


class Worklog_By_Tasks:
    def __init__(self,
                 configuration: Configuration,
                 start_time: datetime,
                 end_time: datetime,
                 issue_tracker: Jira_Connection,
                 outlook: Outlook_Connection,
                 worklog_service: Worklog_Service):
        self.worklogs_service = worklog_service
        self.configuration = configuration
        self.start_time = start_time
        self.end_time = end_time
        self.issue_tracker = issue_tracker
        self.outlook = outlook

    def modify(self):
        tasks = self.outlook.get_tasks(self.start_time, self.end_time)
        if len(tasks) == 0:
            print('Not tasks.')
            return

        self.check_issues(tasks)

        date_generated = [self.start_time + timedelta(days=x) for x in range(0, (self.end_time - self.start_time).days)]
        for date in date_generated:
            if not supported_day(date):
                continue

            wrote_time = self.worklogs_service.get_summary_by_datetime(date)
            while wrote_time < NEEDS_HOURS:
                task, diff = self.get_correct_task(tasks, date, wrote_time)

                if task is None:
                    break
                wrote_time += diff

    def get_correct_task(self, tasks: list[Outlook_Task], current_date: datetime, wrote_time: float):
        tasks_without_time = []

        for task_item in tasks:
            if task_item.start_date > current_date.date():
                continue

            if task_item.limit_time is None:
                tasks_without_time.append(task_item)
                tasks.remove(task_item)

        for task_item in tasks:
            if task_item.wrote_time >= task_item.limit_time:
                task_item.close()
                tasks.remove(task_item)
                continue

            need_write_time = 0
            if task_item.limit_time + wrote_time > NEEDS_HOURS:
                need_write_time = NEEDS_HOURS - wrote_time
            else:
                need_write_time += task_item.limit_time

            self.worklogs_service.add_worklog(task_item.name, current_date, task_item.jira_issue, need_write_time)
            task_item.update_name(need_write_time)

            return task_item, need_write_time

        if len(tasks_without_time) != 0:
            need_write_time = 8 - wrote_time
            task_item = random.choice(tasks_without_time)
            self.worklogs_service.add_worklog(task_item.name, current_date, task_item.jira_issue, need_write_time)
            task_item.update_name(need_write_time)
            return task_item, need_write_time
        return None, 0

    def check_issues(self, tasks):
        for task in tasks:
            if task.jira_issue is not None:
                continue

            task_categories = task.get_categories()

            if task_categories is None:
                category = self.configuration.categories[None]
            else:
                if task_categories[0] not in self.configuration.categories:
                    category = self.configuration.categories[None]
                else:
                    category = self.configuration.categories[task_categories[0]]

            parent_issue_id = category.jira_issue_id
            new_issue = self.issue_tracker.create_subtask(task.name, parent_issue_id)
            task.update_issue_id(new_issue.key)
