import datetime
import os

from core.helpers.scheduleService import ScheduleService
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.tracks.add_new_track_request import AddNewTrackRequest
from core.rabbitmq.messages.configuration.tracks.get_track_by_id_request import GetTrackRequest, \
    YANDEX_MUSIC_SOURCE
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from yandex.models.track_dto import TrackDto
from yandex.services.tags_service import TagsService
from yandex.services.yandex_service import YandexMusicService


class DownloadLikesTracksHandler(ScheduleService):
    def __init__(self, yandexMusicService: YandexMusicService, trackService: TagsService, logger_Service: Logger_Service, rpcPublisher: RpcPublisher):
        super().__init__(logger_Service, 12)
        self.rpcPublisher = rpcPublisher
        self.logger_Service = logger_Service
        self.trackService = trackService
        self.yandexMusicService = yandexMusicService

    def update(self):
        self.logger_Service.info(self.TAG, f'Update {datetime.datetime.now()}')
        tracks: list[TrackDto] = self.yandexMusicService.get_songs()

        # history_tracks = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTracksRequest())
        # if history_tracks.status == ERROR_STATUS_CODE:
        #     raise Exception(history_tracks.message)

        # downloaded_tracks: list[TrackModel] = []
        # for track in history_tracks.message:
        #     downloaded_tracks.append(TrackModel.deserialize(track))

        for track in tracks:
            track_model_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTrackRequest(track.id, YANDEX_MUSIC_SOURCE))

            if track_model_response.status == ERROR_STATUS_CODE:
                # Change name of the final file here

                track_storage_dto = self.yandexMusicService.download(track)

                self.trackService.set_metadata(track, track_storage_dto)
                os.remove(track_storage_dto.cover_path)
                add_track_model_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, AddNewTrackRequest(track.id, track_storage_dto.track_name, YANDEX_MUSIC_SOURCE))
                if add_track_model_response.status == ERROR_STATUS_CODE:
                    raise Exception(add_track_model_response.message)



