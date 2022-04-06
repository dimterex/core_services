from datetime import timedelta, datetime

import dateutil.parser

from modules.connections.jira_connection import Jira_Connection
from modules.models.configuration import Configuration
from modules.models.task_entry import Task_Entry
from modules.worklog_core.services.worklog_service import Worklog_Service

from todoist_api_python.api import TodoistAPI
from todoist_api_python.endpoints import get_sync_url
from todoist_api_python.http_requests import get

from modules.models.todoist_tasks import Todoist_Tasks


NEEDS_HOURS = 8

class Worklog_By_Tasks_v2:
    def __init__(self,
                 configuration: Configuration,
                 start_time: datetime,
                 issue_tracker: Jira_Connection,
                 todoistAPI: TodoistAPI,
                 worklog_service: Worklog_Service):
        self.todoistAPI = todoistAPI
        self.worklogs_service = worklog_service
        self.configuration = configuration
        self.start_time = start_time
        self.issue_tracker = issue_tracker

    def modify(self):
        print('Worklog_By_Tasks_v2. Starting modify')
        completed_tasks = self.get_competed_tasks()

        if len(completed_tasks) == 0:
            print('Not tasks.')
            return

        self.check_issues(completed_tasks)

        wrote_time = self.worklogs_service.get_summary()

        tasks_time = (NEEDS_HOURS - wrote_time) / len(completed_tasks)
        for task in completed_tasks:
            self.worklogs_service.add_worklog(task.name, self.start_time, f'{task.jira_issue}', tasks_time)
        print('Worklog_By_Tasks_v2. Ending modify')

    def check_issues(self, tasks: list[Task_Entry]):
        for task in tasks:
            if task.jira_issue is not None:
                continue

            if task.category is None:
                category = self.configuration.tasks_categories[None]
            else:
                if task.category not in self.configuration.tasks_categories:
                    category = self.configuration.tasks_categories[None]
                else:
                    category = self.configuration.tasks_categories[task.category]

            parent_issue_id = category.jira_issue_id
            new_issue = self.issue_tracker.create_subtask(task.name, parent_issue_id)
            task.jira_issue = new_issue.key
            self.update_task(task.id, new_issue.key)

    def get_competed_tasks(self):
        endpoint = get_sync_url('completed/get_all')
        tasks = get(self.todoistAPI._session, endpoint, self.todoistAPI._token, {})
        correct_tasks = []
        for task in Todoist_Tasks(tasks).items:
            taskInfo = self.todoistAPI.get_task(task.task_id)
            if taskInfo.section_id == 0:
                sectionInfo = self.todoistAPI.get_section(83787255)
            else:
                sectionInfo = self.todoistAPI.get_section(taskInfo.section_id)
            # print('--------')
            # print(taskInfo.content)
            if taskInfo.due is None:
                continue
            date = dateutil.parser.parse(taskInfo.due.date)
            # print(date.day, self.start_time.day)
            # print(date.month, self.start_time.month)
            # print(date.year, self.start_time.year)
            if date.day == self.start_time.day and date.month == self.start_time.month and date.year == self.start_time.year:
                if len(taskInfo.label_ids) > 0:
                    label = self.todoistAPI.get_label(taskInfo.label_ids[0])
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, sectionInfo.name, label.name))
                else:
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, sectionInfo.name, None))

        return correct_tasks

    def update_task(self, taskId, jira_issue):
        labels = self.todoistAPI.get_labels()
        label_id = None

        for label in labels:
            if label.name == jira_issue:
                label_id = label.id
                break

        if label_id is None:
            label = self.todoistAPI.add_label(jira_issue)
            label_id = label.id

        self.todoistAPI.update_task(taskId, label_ids=[label_id])
