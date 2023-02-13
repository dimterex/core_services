from configuration.database.meeting_categories_table import MeetingCategoriesTable
from modules.core.rabbitmq.messages.configuration.meeting_categories.remove_meeting_categories_request import \
    REMOVE_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE, RemoveMeetingCategoriesRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveMeetingCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: MeetingCategoriesTable):
        super().__init__(REMOVE_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveMeetingCategoriesRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
