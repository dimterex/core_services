from configuration.database.todoist_categories_table import TodoistCategoriesTable
from modules.core.rabbitmq.messages.configuration.todoits_categories.set_todoits_categories_request import \
    SET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE, SetTodoistCategoriesRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetTodoitsCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TodoistCategoriesTable):
        super().__init__(SET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetTodoistCategoriesRequest.deserialize(payload)
            self.storage.set_todoist_categories(request.categories)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
