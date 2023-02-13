from configuration.database.configuration_storage import ConfigurationStorage
from configuration.database.meeting_categories_table import MeetingCategoriesTable
from configuration.database.periodical_tasks_table import periodical_tasks_table
from modules.core.rabbitmq.messages.configuration.meeting_categories.add_new_meeting_category_request import \
    ADD_NEW_MEETING_CATEGORY_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.configuration.meeting_categories.get_meeting_categories_request import \
    GET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.configuration.periodical_tasks.add_new_periodical_task_request import \
    ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewPeriodicalTaskRequestHandler(RpcBaseHandler):
    def __init__(self, storage: periodical_tasks_table):
        super().__init__(ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_task()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
