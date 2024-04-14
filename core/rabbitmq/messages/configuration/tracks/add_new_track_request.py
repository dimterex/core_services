from core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_TRACK_REQUEST_MESSAGE_TYPE = 'add_new_track_request'
ADD_NEW_TRACK_REQUEST_TRACK_ID = 'id'
ADD_NEW_TRACK_REQUEST_TRACK_NAME = 'name'
ADD_NEW_TRACK_REQUEST_TRACK_SOURCE = 'source'


class AddNewTrackRequest(BaseMessage):
    def __init__(self, track_id: str, name: str, source: str):
        super().__init__(ADD_NEW_TRACK_REQUEST_MESSAGE_TYPE)
        self.name = name
        self.track_id = track_id
        self.source = source

    def serialize(self):
        return self.to_json({
            ADD_NEW_TRACK_REQUEST_TRACK_ID: self.track_id,
            ADD_NEW_TRACK_REQUEST_TRACK_NAME: self.name,
            ADD_NEW_TRACK_REQUEST_TRACK_SOURCE: self.source,
        })

    @staticmethod
    def deserialize(payload):
        id = payload[ADD_NEW_TRACK_REQUEST_TRACK_ID]
        name = payload[ADD_NEW_TRACK_REQUEST_TRACK_NAME]
        source = payload[ADD_NEW_TRACK_REQUEST_TRACK_SOURCE]
        return AddNewTrackRequest(id, name, source)
