from core.rabbitmq.messages.base_request import BaseMessage

REMOVE_TRACKS_REQUEST_MESSAGE_TYPE = 'remove_tracks_request'
REMOVE_TRACKS_REQUEST_IDS = 'ids'


class RemoveTracksRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_TRACKS_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_TRACKS_REQUEST_IDS: self.ids
        })

    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_TRACKS_REQUEST_IDS]
        return RemoveTracksRequest(ids)
