from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.messages.status_response import StatusResponse, ERROR_STATUS_CODE
from modules.core.rabbitmq.messages.todoist.update_label_request import UPDATE_LABEL_MESSAGE_TYPE, \
    UPDATE_LABEL_TODOIST_TASK_ID, UPDATE_LABEL_TODOIST_TASK_LABEL
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL, INFO_LOG_LEVEL
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


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
        labels = self.todoistAPI.get_labels()

        for label in labels:
            if label.name == task_label:
                status_message = f'Label {task_label} exist in {task_id}'
                self.logger_service.info(self.TAG, status_message)
                return StatusResponse(status_message)

        label = self.todoistAPI.add_label(task_label)
        label_id = label.id

        self.todoistAPI.update_task(int(task_id), label_ids=[label_id])

        status_message = f'Label {task_label} added to {task_id}'
        self.logger_service.debug(self.TAG, status_message)
        return StatusResponse(status_message)

