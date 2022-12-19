from configuration.database.configuration_storage import ConfigurationStorage
from modules.core.rabbitmq.messages.configuration.meeting_categories.get_meeting_categories_request import \
    GET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetMeetingCategoriesRequestHandler(RpcBaseHandler):
    def __init__(self, storage: ConfigurationStorage):
        super().__init__(GET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            categories = self.storage.get_meeting_categories()
            js = []
            for category in categories:
                js.append(category.serialize())
            return StatusResponse(js)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)