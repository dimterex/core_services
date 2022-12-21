from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.configuration.meeting_categories.get_meeting_categories_request import GetMeetingCategoriesRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.get_meeting_categories_reponse import MeetingCategoriesResponse


class GetMeetingsCategoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetMeetingCategoriesRequest())

        result = MeetingCategoriesResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.categories = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
