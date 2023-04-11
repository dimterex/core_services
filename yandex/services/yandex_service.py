import os

from yandex_music import Client, Search, Track

from modules.core.log_service.log_service import Logger_Service
from yandex.models.track_dto import TrackDto
from yandex.models.track_storage_dto import TrackStorageDto


class YandexMusicService:
    def __init__(self, token: str, download_directory: str, logger_Service: Logger_Service):
        self.download_directory = download_directory
        self.logger_Service = logger_Service
        self.token = token
        self.TAG = self.__class__.__name__

    def find_track(self, query) -> Search:
        client = Client(self.token).init()
        type_to_name = {
            'track': 'трек',
            'artist': 'исполнитель',
            'album': 'альбом',
            'playlist': 'плейлист',
            'video': 'видео',
            'user': 'пользователь',
            'podcast': 'подкаст',
            'podcast_episode': 'эпизод подкаста',
        }

        search_result = client.search(query)

        text = [f'Результаты по запросу "{query}":', '']

        best_result_text = ''
        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result

            text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

            if type_ in ['track', 'podcast_episode']:
                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(f'Содержимое лучшего результата: {best_result_text}\n')

        if search_result.artists:
            text.append(f'Исполнителей: {search_result.artists.total}')
        if search_result.albums:
            text.append(f'Альбомов: {search_result.albums.total}')
        if search_result.tracks:
            text.append(f'Треков: {search_result.tracks.total}')
        if search_result.playlists:
            text.append(f'Плейлистов: {search_result.playlists.total}')
        if search_result.videos:
            text.append(f'Видео: {search_result.videos.total}')

        text.append('')
        self.logger_Service.debug(self.TAG, '\n'.join(text))
        return search_result

    def get_songs(self) -> list[TrackDto]:
        client = Client(self.token).init()
        if not client.me.plus.has_plus:
            return []
        tracks = client.users_likes_tracks()
        response: list[TrackDto] = []
        for t in tracks:
            track: Track = client.tracks(t.id)[0]
            response.append(TrackDto(track))
        return response

    def download(self, track_id: str, name: str) -> TrackStorageDto:
        self.logger_Service.debug(self.TAG, f'Start download: {name}')
        client = Client(self.token).init()
        track = client.tracks(track_id)[0]
        track_storage_dto = TrackStorageDto(os.path.join(self.download_directory, f'{name}.mp3'), os.path.join(self.download_directory, f'{name}.png'))
        track.download_cover(track_storage_dto.cover_path, '1000x1000')
        track.download(track_storage_dto.file_path, 'mp3', 320)
        self.logger_Service.debug(self.TAG, f'End download: {name}')
        return track_storage_dto
