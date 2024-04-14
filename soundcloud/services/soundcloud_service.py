import json
import os
from pathlib import Path

import requests

from core.log_service.log_service import Logger_Service
from soundcloud.models.track_dto import TrackDto
from sclib import SoundcloudAPI


class SoundCloudService:

    def __init__(self, download_directory: str, logger_Service: Logger_Service):
        self.download_directory = download_directory
        self.logger_Service = logger_Service
        self.TAG = self.__class__.__name__

    def try_to_get_something(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    def get_songs(self, soundcloud_client_id_response: str, soundcloud_user_id_response: str) -> list[TrackDto]:
        user_id = soundcloud_user_id_response
        client_id = soundcloud_client_id_response
        limit = 24

        url = f'https://api-v2.soundcloud.com/users/{user_id}/likes?client_id={client_id}&limit={limit}'

        iteration = 0
        count = 3
        collection = None
        tracks: [TrackDto] = []
        while iteration < count:
            result = self.try_to_get_something(url)

            if result is None:
                iteration += 1
            else:
                collection = result['collection']
                break

        if collection is None:
            return tracks

        for item in collection:
            if 'track' in item:
                track = item['track']
                tracks.append(TrackDto(track))
        return tracks

    def download(self, track_dto: TrackDto) -> str:
        api = SoundcloudAPI()
        track = api.resolve(track_dto.url)

        track_file_name = f'{track.title}.mp3'

        track_path = os.path.join(self.download_directory, str(track.id))
        track_name = os.path.join(track_path,track_file_name)
        filename_meta_path = os.path.join(track_path, f'{track.title}.json')

        Path(track_path).mkdir(parents=True, exist_ok=True)

        self.logger_Service.debug(self.TAG, f'Start download: {track.title}')
        with open(track_name, 'wb+') as file:
            track.write_mp3_to(file)
        with open(filename_meta_path, 'w', encoding='utf-8') as file:
            json.dump({
                'permalink_url': track.permalink_url,
                'purchase_url': track.purchase_url,
                'artist': track.artist,
                'album': track.album,
                'artwork_url': track.artwork_url,
                'created_at': track.created_at,
                'id': track.id,
                'publisher_metadata': track.publisher_metadata,
                'release_date': track.release_date,
                'title': track.title,
            }, file, ensure_ascii=False, indent=4)

        self.logger_Service.debug(self.TAG, f'Success download: {track.title}')

        return track_file_name
