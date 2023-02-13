from configuration.database.todoist_categories_table import TodoistCategoriesTable
from modules.core.rabbitmq.messages.configuration.todoits_categories.get_todoits_categories_request import \
    GET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetTodoistCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TodoistCategoriesTable):
        super().__init__(GET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            categories = self.storage.get_task_categories()
            js = []
            for category in categories:
                js.append(category.serialize())
            return StatusResponse(js)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
