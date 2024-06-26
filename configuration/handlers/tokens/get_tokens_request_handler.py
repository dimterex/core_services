from configuration.database.tokens_table import TokensTable
from core.rabbitmq.messages.configuration.tokens.get_tokens_request import GET_TOKENS_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetTokensRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TokensTable):
        super().__init__(GET_TOKENS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            tokens = self.storage.get_tokens()
            js = []
            for token in tokens:
                js.append(token.serialize())
            return StatusResponse(js)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
