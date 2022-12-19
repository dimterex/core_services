from configuration.database.configuration_storage import ConfigurationStorage
from modules.core.rabbitmq.messages.configuration.urls.get_urls_request import GET_URLS_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetUrlsRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: ConfigurationStorage):
        super().__init__(GET_URLS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            urls = self.storage.get_urls()
            return StatusResponse(urls)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
