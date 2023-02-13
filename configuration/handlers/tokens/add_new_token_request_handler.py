from configuration.database.tokens_table import TokensTable
from modules.core.rabbitmq.messages.configuration.tokens.add_new_token_request import ADD_NEW_TOKEN_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewTokenRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TokensTable):
        super().__init__(ADD_NEW_TOKEN_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_token()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
