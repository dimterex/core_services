from configuration.database.urls_table import UrlsTable
from modules.core.rabbitmq.messages.configuration.urls.get_urls_request import GET_URLS_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetUrlsRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: UrlsTable):
        super().__init__(GET_URLS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            urls = self.storage.get_urls()
            response = []
            for url in urls:
                response.append(url.serialize())
            return StatusResponse(response)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
