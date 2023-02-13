from configuration.database.todoist_categories_table import TodoistCategoriesTable
from modules.core.rabbitmq.messages.configuration.todoits_categories.remove_todoist_categories_request import \
    REMOVE_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE, RemoveTodoistCategoriesRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveTodoistCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TodoistCategoriesTable):
        super().__init__(REMOVE_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveTodoistCategoriesRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
