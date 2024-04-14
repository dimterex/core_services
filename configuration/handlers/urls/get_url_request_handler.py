from configuration.database.urls_table import UrlsTable
from core.rabbitmq.messages.configuration.urls.get_url_request import GET_URL_REQUEST_MESSAGE_TYPE, GetUrlRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetUrlRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: UrlsTable):
        super().__init__(GET_URL_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = GetUrlRequest.deserialize(payload)
            url = self.storage.get_url(request.url_type)
            return StatusResponse(url)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
