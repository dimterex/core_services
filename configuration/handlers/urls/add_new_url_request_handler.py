from configuration.database.urls_table import UrlsTable
from core.rabbitmq.messages.configuration.urls.add_new_url_request import ADD_NEW_URL_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewUrlRequestHandler(RpcBaseHandler):
    def __init__(self, storage: UrlsTable):
        super().__init__(ADD_NEW_URL_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_url()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
