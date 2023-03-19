TRACK_MODEL_TRACK_ID = 'track_id'
TRACK_MODEL_NAME = 'name'
TRACK_MODEL_ID = 'id'


class TrackDatabaseModel:
    def __init__(self, id: int, track_id: str, name: str):
        self.track_id = track_id
        self.id = id
        self.name = name

    def serialize(self) -> dict:
        return {
            TRACK_MODEL_ID: self.id,
            TRACK_MODEL_NAME: self.name,
            TRACK_MODEL_TRACK_ID: self.track_id,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[TRACK_MODEL_ID]
        name = payload[TRACK_MODEL_NAME]
        track_id = payload[TRACK_MODEL_TRACK_ID]
        return TrackDatabaseModel(id, track_id, name)
