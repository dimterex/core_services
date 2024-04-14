from configuration.database.tokens_table import TokensTable
from core.rabbitmq.messages.configuration.tokens.get_token_request import GET_TOKEN_REQUEST_MESSAGE_TYPE, \
    GetTokenRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetTokenRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TokensTable):
        super().__init__(GET_TOKEN_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = GetTokenRequest.deserialize(payload)
            token = self.storage.get_token(request.key)
            return StatusResponse(token)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
