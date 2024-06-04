from configuration.database.iptv_duplicate_list_table import IptvDuplicateListTable
from core.rabbitmq.messages.configuration.iptv_duplicate_list.get_duplicate_list_request import \
    GET_IPTV_DUPLICATE_LIST_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetDuplicateListRequestHandler(RpcBaseHandler):
    def __init__(self, storage: IptvDuplicateListTable):
        super().__init__(GET_IPTV_DUPLICATE_LIST_REQUEST_MESSAGE_TYPE)
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
