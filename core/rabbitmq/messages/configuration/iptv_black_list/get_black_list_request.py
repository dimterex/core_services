from core.rabbitmq.messages.base_request import BaseMessage

GET_IPTV_BLACK_LIST_REQUEST_MESSAGE_TYPE = 'get_iptv_black_list_request'


class GetIptvBlackListRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_IPTV_BLACK_LIST_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
