from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.configuration.tokens.get_tokens_request import GetTokensRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.get_tokens_reponse import TokensResponse


class GetTokensRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTokensRequest())

        result = TokensResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.tokens = response.message
        else:
            result.exception = response.message

        contentType = 'application/json; charset=utf-8'
        return self.generate_success(contentType, result)
