from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.configuration.token_model import TokenModel
from modules.core.rabbitmq.messages.configuration.tokens.set_tokens_request import SetTokensRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class SetTokensRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        body = req.body
        tokens: list[TokenModel] = []
        for b in body:
            tokens.append(TokenModel.deserialize(b))

        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, SetTokensRequest(tokens))
        result = SetBaseResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success updated'
        else:
            result.exception = response.message
        contentType = 'application/json; charset=utf-8'
        return self.generate_success(contentType, result)
