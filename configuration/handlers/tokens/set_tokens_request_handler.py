from configuration.database.tokens_table import TokensTable
from core.rabbitmq.messages.configuration.tokens.set_tokens_request import SET_TOKENS_REQUEST_MESSAGE_TYPE, \
    SetTokensRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetTokensRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TokensTable):
        super().__init__(SET_TOKENS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetTokensRequest.deserialize(payload)
            self.storage.set_tokens(request.tokens)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
