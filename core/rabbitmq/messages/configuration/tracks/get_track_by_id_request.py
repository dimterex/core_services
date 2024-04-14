from core.rabbitmq.messages.base_request import BaseMessage

GET_TRACK_REQUEST_MESSAGE_TYPE = 'get_track_request'
GET_TRACK_REQUEST_TRACK_ID = 'id'
GET_TRACK_REQUEST_TRACK_SOURCE = 'source'

YANDEX_MUSIC_SOURCE = 'yandex'
SOUNDCLOUD_SOURCE = 'soundcloud'


class GetTrackRequest(BaseMessage):
    def __init__(self, track_id: str, source: str):
        super().__init__(GET_TRACK_REQUEST_MESSAGE_TYPE)
        self.track_id = track_id
        self.source = source

    def serialize(self):
        return self.to_json({
            GET_TRACK_REQUEST_TRACK_ID: self.track_id,
            GET_TRACK_REQUEST_TRACK_SOURCE: self.source,
        })

    @staticmethod
    def deserialize(payload):
        id = payload[GET_TRACK_REQUEST_TRACK_ID]
        source = payload[GET_TRACK_REQUEST_TRACK_SOURCE]
        return GetTrackRequest(id, source)
