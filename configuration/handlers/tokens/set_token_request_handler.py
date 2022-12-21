from configuration.database.configuration_storage import ConfigurationStorage
from modules.core.rabbitmq.messages.configuration.tokens.set_token_request import SET_TOKEN_REQUEST_MESSAGE_TYPE, \
    SetTokenRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetTokenRequestHandler(RpcBaseHandler):
    def __init__(self, storage: ConfigurationStorage):
        super().__init__(SET_TOKEN_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = SetTokenRequest.deserialize(payload)
            self.storage.set_token(request.token)
            return StatusResponse('Done')
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
