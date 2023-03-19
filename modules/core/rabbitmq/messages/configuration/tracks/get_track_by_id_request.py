from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_TRACK_REQUEST_MESSAGE_TYPE = 'get_track_request'
GET_TRACK_REQUEST_TRACK_ID = 'id'


class GetTrackRequest(BaseMessage):
    def __init__(self, track_id: str):
        super().__init__(GET_TRACK_REQUEST_MESSAGE_TYPE)
        self.track_id = track_id

    def serialize(self):
        return self.to_json({
            GET_TRACK_REQUEST_TRACK_ID: self.track_id,
        })

    @staticmethod
    def deserialize(payload):
        id = payload[GET_TRACK_REQUEST_TRACK_ID]
        return GetTrackRequest(id)
