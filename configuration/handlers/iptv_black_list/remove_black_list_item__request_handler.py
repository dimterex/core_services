from configuration.database.iptv_black_list_table import IptvBlackListTable
from core.rabbitmq.messages.configuration.iptv_black_list.remove_black_list_item_request import \
    RemoveBlackListItemRequest, REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveBlackListItemRequestHandler(RpcBaseHandler):
    def __init__(self, storage: IptvBlackListTable):
        super().__init__(REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveBlackListItemRequest.deserialize(payload)
            self.storage.remove([request.id])
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
