from configuration.database.meeting_categories_table import MeetingCategoriesTable
from core.rabbitmq.messages.configuration.meeting_categories.add_new_meeting_category_request import \
    ADD_NEW_MEETING_CATEGORY_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewMeetingCategoryRequestHandler(RpcBaseHandler):
    def __init__(self, storage: MeetingCategoriesTable):
        super().__init__(ADD_NEW_MEETING_CATEGORY_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_meeting_category()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
