from configuration.database.iptv_black_list_table import IptvBlackListTable
from core.rabbitmq.messages.configuration.iptv_black_list.add_black_list_item_request import \
    ADD_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddBlackListItemRequestHandler(RpcBaseHandler):
    def __init__(self, storage: IptvBlackListTable):
        super().__init__(ADD_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            new_id = self.storage.add_new_item()
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
