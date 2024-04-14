from configuration.database.base_table import BaseTable
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.track_model import TrackDatabaseModel

ID_COLUMN_NAME = 'id'

TABLE_NAME = 'tracks'
TRACK_ID_COLUMN_NAME = 'track_id'
TRACK_NAME_COLUMN_NAME = 'name'
TRACK_SOURCE_COLUMN_NAME = 'source'


class TracksTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TRACK_ID_COLUMN_NAME} TEXT NOT NULL,
                                {TRACK_NAME_COLUMN_NAME} TEXT NULL,
                                {TRACK_SOURCE_COLUMN_NAME} TEXT NOT NULL);'''

    def get_tracks(self) -> list[TrackDatabaseModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(TrackDatabaseModel(row[0], row[1], row[2]))
        return models

    def get_track_by_track_id(self, track_id: str, source: str) -> TrackDatabaseModel:
        result = self.get_first({
            TRACK_ID_COLUMN_NAME: track_id,
            TRACK_SOURCE_COLUMN_NAME: source,
        })
        if result is None:
            raise Exception(f'Can not find track for {track_id}')

        return TrackDatabaseModel(result[0], result[1], result[2])

    def add_new_track(self, track_id: str, name: str, source: str):
        return self.insert({
            TRACK_ID_COLUMN_NAME: track_id,
            TRACK_NAME_COLUMN_NAME: name,
            TRACK_SOURCE_COLUMN_NAME: source,
        })
