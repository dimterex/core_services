from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from modules.core.rabbitmq.messages.configuration.credentials.set_credentials_request import SetCredentialsRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class SetCredentialsRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        body = await request.json()
        credentialModel = CredentialModel.deserialize(body)
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, SetCredentialsRequest(credentialModel))

        result = SetBaseResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success updated'
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
