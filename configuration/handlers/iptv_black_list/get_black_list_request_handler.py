from configuration.database.iptv_black_list_table import IptvBlackListTable
from core.rabbitmq.messages.configuration.iptv_black_list.get_black_list_request import \
    GET_IPTV_BLACK_LIST_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetBlackListRequestHandler(RpcBaseHandler):
    def __init__(self, storage: IptvBlackListTable):
        super().__init__(GET_IPTV_BLACK_LIST_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            data = self.storage.get_black_list()
            response = []
            for item in data:
                response.append(item.serialize())
            return StatusResponse(response)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
