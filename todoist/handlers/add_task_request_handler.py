from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.messages.configuration.todoits_categories.add_new_todoist_task_request import \
    ADD_NEW_TODOIST_TASK_REQUEST_MESSAGE_TYPE, AddNewTodoistTaskRequest
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddTaskRequestHandler(RpcBaseHandler):
    def __init__(self, todoist: TodoistAPI, logger_service: Logger_Service):
        super().__init__(ADD_NEW_TODOIST_TASK_REQUEST_MESSAGE_TYPE)
        self.logger_service = logger_service
        self.todoistAPI = todoist
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:

        request = AddNewTodoistTaskRequest.deserialize(payload)

        self.logger_service.debug(self.TAG, f'Starting add new task {request.name} with {request.issue_id}')
        labels = self.todoistAPI.get_labels()

        issue_label = next((label for label in labels if label.name == request.issue_id), None)

        if issue_label is None:
            issue_label = self.todoistAPI.add_label(request.issue_id)

        project_id = self.todoistAPI.get_projects()[-1].id

        task = self.todoistAPI.add_task(request.name, project_id=project_id, due_string="today", labels=[issue_label.name])

        status_message = f'Label {request.issue_id} added to {task.id}'
        self.logger_service.debug(self.TAG, status_message)
        return StatusResponse(status_message)
