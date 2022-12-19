from configuration.database.configuration_storage import ConfigurationStorage
from modules.core.rabbitmq.messages.configuration.urls.set_urls_request import SET_URL_REQUEST_MESSAGE_TYPE, SetUrlsRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetUrlRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: ConfigurationStorage):
        super().__init__(SET_URL_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetUrlsRequest.deserialize(payload)
            self.storage.set_urls(request.models)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)

