from core.rabbitmq.messages.base_request import BaseMessage

GET_IPTV_EPG_SOURCES_REQUEST_MESSAGE_TYPE = 'get_iptv_epg_sources_request'


class GetIptvEpgSourcesRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_IPTV_EPG_SOURCES_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
