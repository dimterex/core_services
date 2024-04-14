from todoist_api_python.api import TodoistAPI

from core.rabbitmq.messages.status_response import StatusResponse
from core.rabbitmq.messages.todoist.update_label_request import UPDATE_LABEL_MESSAGE_TYPE, \
    UPDATE_LABEL_TODOIST_TASK_ID, UPDATE_LABEL_TODOIST_TASK_LABEL
from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class UpdateLabelRequestHandler(RpcBaseHandler):
    def __init__(self, todoist: TodoistAPI, logger_service: Logger_Service):
        super().__init__(UPDATE_LABEL_MESSAGE_TYPE)
        self.logger_service = logger_service
        self.todoistAPI = todoist
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        task_id = payload[UPDATE_LABEL_TODOIST_TASK_ID]
        task_label = payload[UPDATE_LABEL_TODOIST_TASK_LABEL]

        self.logger_service.debug(self.TAG, f'Starting add label {task_label} to {task_id}')
        current_task = self.todoistAPI.get_task(task_id)

        status_messages = []

        if task_label in current_task.labels:
            status_messages.append(f'Label {task_label} exist in {task_id}')
        else:
            self.todoistAPI.update_task(current_task.id, labels=[task_label])

        tasks = self.todoistAPI.get_tasks()
        for task in tasks:
            if task.content == current_task.content:
                self.todoistAPI.update_task(task.id, labels=[task_label])
                status_messages.append(f'Label {task_label} added to {task_id}')

        self.logger_service.info(self.TAG, status_messages)
        return StatusResponse(status_messages)
