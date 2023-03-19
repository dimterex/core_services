from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_TRACKS_REQUEST_MESSAGE_TYPE = 'get_tracks_request'


class GetTracksRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_TRACKS_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
