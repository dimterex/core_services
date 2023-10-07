from datetime import datetime

import dateutil.parser

from todoist_api_python.api import TodoistAPI
from todoist_api_python.endpoints import get_sync_url
from todoist_api_python.http_requests import get
from todoist_api_python.models import Task

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.rabbitmq.messages.status_response import StatusResponse, ERROR_STATUS_CODE
from modules.core.rabbitmq.messages.todoist.get_completed_tasks_request import COMPLETED_TASKS_REQUEST_MESSAGE_TYPE, \
    COMPLETED_TASKS_REQUEST_DATE_PROPERTY
from modules.core.log_service.log_service import DEBUG_LOG_LEVEL, Logger_Service, INFO_LOG_LEVEL, TRACE_LOG_LEVEL
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from todoist.models.task_entry import Task_Entry
from todoist.models.todoist_tasks import Todoist_Tasks


class GetCompletedTasksRequestHandler(RpcBaseHandler):
    def __init__(self, todoist: TodoistAPI, logger_service: Logger_Service):
        super().__init__(COMPLETED_TASKS_REQUEST_MESSAGE_TYPE)
        self.logger_service = logger_service
        self.todoistAPI = todoist
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        start_time = convert_rawdate_to_datetime(payload[COMPLETED_TASKS_REQUEST_DATE_PROPERTY])

        self.logger_service.debug(self.TAG, 'Starting modify')

        try:
            completed_tasks = self.get_competed_tasks(start_time)

            if len(completed_tasks) == 0:
                self.logger_service.info(self.TAG, 'Not tasks.')

            self.logger_service.debug(self.TAG, 'Ending modify')
            issues = []
            for issue in completed_tasks:
                issues.append(issue.serialize())

            return StatusResponse(issues)

        except Exception as e:
            return StatusResponse(str(e), ERROR_STATUS_CODE)
        finally:
            self.logger_service.debug(self.TAG, 'Ended')

    def get_competed_tasks(self, start_time: datetime):
        day = str(start_time.day)
        if len(day) == 1:
            day = f'0{day}'

        endpoint = get_sync_url(f'completed/get_all?since={start_time.year}-{start_time.month}-{day}T00:01')
        tasks = get(self.todoistAPI._session, endpoint, self.todoistAPI._token, {})

        correct_tasks = []
        for task_id in Todoist_Tasks(tasks).items:
            taskInfo: Task = self.todoistAPI.get_task(task_id)
            self.logger_service.trace(self.TAG, str(taskInfo))
            category = None
            if taskInfo.section_id is not None and taskInfo.section_id > 0:
                category = self.todoistAPI.get_section(taskInfo.section_id).name
            if taskInfo.due is None:
                continue
            date = dateutil.parser.parse(taskInfo.due.date)

            if date.day == start_time.day and date.month == start_time.month and date.year == start_time.year:
                if len(taskInfo.labels) > 0:
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, category, taskInfo.labels[0]))
                else:
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, category, None))

        return correct_tasks
