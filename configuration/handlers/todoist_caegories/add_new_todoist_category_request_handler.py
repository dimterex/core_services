from configuration.database.todoist_categories_table import TodoistCategoriesTable
from modules.core.rabbitmq.messages.configuration.todoits_categories.add_new_todoist_category_request import \
    ADD_NEW_TODOIST_CATEGORY_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewTodoistCategoryRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TodoistCategoriesTable):
        super().__init__(ADD_NEW_TODOIST_CATEGORY_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_category()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
