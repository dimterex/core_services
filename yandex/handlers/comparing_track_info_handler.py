import csv
import datetime
import os
import re
import threading

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.identificators import TRACKS_QUEUE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from modules.core.rabbitmq.messages.tracks.get_track_metadata_request import GetTrackMetadataRequest
from modules.core.rabbitmq.messages.tracks.track_model import TrackModel
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from yandex.services.tags_service import TagsService
from yandex.services.yandex_service import YandexMusicService


class ComparingTrackInfoHandler:
    def __init__(self, download_directory: str, yandexMusicService: YandexMusicService, trackService: TagsService, logger_Service: Logger_Service, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher
        self.logger_Service = logger_Service
        self.trackService = trackService
        self.yandexMusicService = yandexMusicService
        self.TAG = self.__class__.__name__
        self.filename = os.path.join(download_directory, 'comparing.csv')

    def start(self, folder_path: str):
        th = threading.Thread(target=self.update(folder_path), name=self.TAG)
        th.start()

    def update(self, folder_path: str):
        self.logger_Service.info(self.TAG, f'Update {datetime.datetime.now()}')

        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow(['file_path',
                             'yandex_title',
                             'current_title',

                             'yandex_albums',
                             'current_albums',

                             'yandex_artists',
                             'current_artists',

                             'yandex_album_artists',
                             'current_album_artists',

                             'yandex_year',
                             'current_year',

                             'yandex_position',
                             'current_position',

                             'yandex_tracks_count',
                             'current_tracks_count',

                             'yandex_cover',
                             'current_cover'])

            for file_path in file_paths:
                file_name = re.sub(r"^\d+\.", "", os.path.splitext(os.path.basename(file_path))[0])
                token_response = self.rpcPublisher.call(TRACKS_QUEUE, GetTrackMetadataRequest(file_name))

                if token_response.status == ERROR_STATUS_CODE:
                    continue

                trackModel = TrackModel.deserialize(token_response.message)
                try:
                    currentModel = self.trackService.get_metadata(file_path)
                except:
                    continue

                writer.writerow([file_path,
                                 trackModel.title,
                                 currentModel.title,
                                 trackModel.albums,
                                 currentModel.albums,
                                 trackModel.artists,
                                 currentModel.artists,
                                 trackModel.album_artists,
                                 currentModel.album_artists,
                                 trackModel.year,
                                 currentModel.year,
                                 trackModel.position,
                                 currentModel.position,
                                 trackModel.tracks_count,
                                 currentModel.tracks_count,
                                 trackModel.cover,
                                 currentModel.cover])
