from configuration.database.tokens_table import TokensTable
from modules.core.rabbitmq.messages.configuration.tokens.remove_tokens_request import \
    REMOVE_TOKENS_REQUEST_MESSAGE_TYPE, RemoveTokensRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveTokensRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TokensTable):
        super().__init__(REMOVE_TOKENS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveTokensRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
