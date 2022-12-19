from configuration.database.configuration_storage import ConfigurationStorage
from modules.core.rabbitmq.messages.configuration.meeting_categories.set_meeting_categories_request import \
    SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE, SetMeetingCategoriesRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetMeetingCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: ConfigurationStorage):
        super().__init__(SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetMeetingCategoriesRequest.deserialize(payload)
            self.storage.set_meeting_categories(request.categories)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)