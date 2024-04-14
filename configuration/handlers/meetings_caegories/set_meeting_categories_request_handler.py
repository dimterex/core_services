from configuration.database.meeting_categories_table import MeetingCategoriesTable
from core.rabbitmq.messages.configuration.meeting_categories.set_meeting_categories_request import \
    SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE, SetMeetingCategoriesRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetMeetingCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: MeetingCategoriesTable):
        super().__init__(SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetMeetingCategoriesRequest.deserialize(payload)
            self.storage.set_meeting_categories(request.categories)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
