from configuration.database.urls_table import UrlsTable
from core.rabbitmq.messages.configuration.urls.remove_url_request import REMOVE_URLS_REQUEST_MESSAGE_TYPE, \
    RemoveUrlsRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveUrlsRequestHandler(RpcBaseHandler):
    def __init__(self, storage: UrlsTable):
        super().__init__(REMOVE_URLS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveUrlsRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
