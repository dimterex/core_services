from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_TRACK_METADATA_REQUEST_MESSAGE_TYPE = 'get_track_metadata_request'
GET_TRACK_METADATA_REQUEST_QUERY = 'query'


class GetTrackMetadataRequest(BaseMessage):
    def __init__(self, query: str):
        super().__init__(GET_TRACK_METADATA_REQUEST_MESSAGE_TYPE)
        self.query = query

    def serialize(self) -> dict:
        return self.to_json({
            GET_TRACK_METADATA_REQUEST_QUERY: self.query,
        })

    @staticmethod
    def deserialize(payload):
        query = payload[GET_TRACK_METADATA_REQUEST_QUERY]
        return GetTrackMetadataRequest(query)
