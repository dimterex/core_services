from core.rabbitmq.messages.base_request import BaseMessage

GET_IPTV_DUPLICATE_LIST_REQUEST_MESSAGE_TYPE = 'get_iptv_duplicate_list_request'


class GetIptvDuplicateListRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_IPTV_DUPLICATE_LIST_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
