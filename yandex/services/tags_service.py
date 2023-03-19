import re

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.tracks.track_model import TrackModel
from yandex.models.track_dto import TrackDto

import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, PictureType

from yandex.models.track_storage_dto import TrackStorageDto


class TagsService:
    def __init__(self, logger_Service: Logger_Service):
        self.TAG = self.__class__.__name__
        self.logger_Service = logger_Service

    def set_metadata(self, track: TrackDto, trackStorageDto: TrackStorageDto):
        self.logger_Service.info(self.TAG, f'Start edit {track.title}')
        try:
            audio = EasyID3(trackStorageDto.file_path)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(trackStorageDto.file_path, easy=True)
            audio.add_tags()

        audio['title'] = track.title
        audio['artist'] = track.artists
        audio['albumartist'] = track.album_artists
        audio['album'] = track.albums
        audio['date'] = track.year
        audio['tracknumber'] = f'{track.track_position}/{track.album_tracks}'

        audio.save()

        # update cover
        file_foobar = MP3(trackStorageDto.file_path)

        with open(trackStorageDto.cover_path, 'rb') as f:
            cover_data = f.read()
            file_foobar['APIC'] = APIC(
                encoding=3,
                mime='image/png',
                type=PictureType.COVER_FRONT,
                data=cover_data
            )

        file_foobar.save()
        self.logger_Service.info(self.TAG, f'End edit {track.title}')

    def get_metadata(self, file_path: str) -> TrackModel:
        audio = EasyID3(file_path)

        tracks_count = re.findall(r'(?<=/)\d+$', audio.get('tracknumber')[0])[0]
        track_position = re.findall(r"^([^/]+)", audio.get('tracknumber')[0])[0]

        return TrackModel(audio.get('title')[0],
                          audio.get('album')[0],
                          audio.get('artist')[0],
                          audio.get('albumartist')[0],
                          audio.get('date')[0],
                          track_position,
                          tracks_count,
                          'not info')
