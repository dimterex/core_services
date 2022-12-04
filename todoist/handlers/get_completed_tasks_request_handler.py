from datetime import datetime

import dateutil.parser

from todoist_api_python.api import TodoistAPI
from todoist_api_python.endpoints import get_sync_url
from todoist_api_python.http_requests import get

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.rabbitmq.messages.todoist.get_completed_tasks_request import COMPLETED_TASKS_REQUEST_MESSAGE_TYPE, \
    COMPLETED_TASKS_REQUEST_DATE_PROPERTY
from modules.core.rabbitmq.messages.todoist.get_completed_tasks_response import GetCompletedTasksResponse
from modules.core.log_service.log_service import DEBUG_LOG_LEVEL, Logger_Service, INFO_LOG_LEVEL
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from todoist.models.task_entry import Task_Entry
from todoist.models.todoist_tasks import Todoist_Tasks


class GetCompletedTasksRequestHandler(RpcBaseHandler):
    def __init__(self, todoist: TodoistAPI, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.todoistAPI = todoist

    def get_message_type(self) -> str:
        return COMPLETED_TASKS_REQUEST_MESSAGE_TYPE

    def execute(self, payload) -> str:
        start_time = convert_rawdate_to_datetime(payload[COMPLETED_TASKS_REQUEST_DATE_PROPERTY])

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Starting modify')
        completed_tasks = self.get_competed_tasks(start_time)

        if len(completed_tasks) == 0:
            self.logger_service.send_log(INFO_LOG_LEVEL, self.__class__.__name__, 'Not tasks.')

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Ending modify')
        response = GetCompletedTasksResponse(completed_tasks)
        return response.to_json()

    def get_competed_tasks(self, start_time: datetime):
        endpoint = get_sync_url(f'completed/get_all?since={start_time.year}-{start_time.month}-{start_time.day}T00:01')
        tasks = get(self.todoistAPI._session, endpoint, self.todoistAPI._token, {})
        # self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, str(tasks))
        correct_tasks = []
        for task in Todoist_Tasks(tasks).items:
            taskInfo = self.todoistAPI.get_task(task.task_id)
            if taskInfo.section_id == 0:
                sectionInfo = self.todoistAPI.get_section(83787255)
            else:
                sectionInfo = self.todoistAPI.get_section(taskInfo.section_id)
            if taskInfo.due is None:
                continue
            date = dateutil.parser.parse(taskInfo.due.date)

            if date.day == start_time.day and date.month == start_time.month and date.year == start_time.year:
                if len(taskInfo.label_ids) > 0:
                    label = self.todoistAPI.get_label(taskInfo.label_ids[0])
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, sectionInfo.name, label.name))
                else:
                    correct_tasks.append(Task_Entry(taskInfo.id, taskInfo.content, date, sectionInfo.name, None))

        return correct_tasks