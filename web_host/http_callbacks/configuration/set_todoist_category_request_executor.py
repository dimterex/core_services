from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.configuration.category_model import CategoryModel
from modules.core.rabbitmq.messages.configuration.meeting_categories.set_meeting_categories_request import SetMeetingCategoriesRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_meeting_categories_reponse import MeetingCategoriesResponse


class SetMeetingsCategoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        body = req.body
        categories: list[CategoryModel] = []
        for b in body:
            categories.append(CategoryModel.deserialize(b))

        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, SetMeetingCategoriesRequest(categories))

        result = MeetingCategoriesResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.categories = response.message
        else:
            result.exception = response.message

        contentType = 'application/json; charset=utf-8'
        return self.generate_success(contentType, result)
