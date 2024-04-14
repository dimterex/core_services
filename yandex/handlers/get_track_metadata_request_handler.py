from yandex_music import Search

from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.status_response import StatusResponse
from core.rabbitmq.messages.tracks.get_track_metadata_request import GET_TRACK_METADATA_REQUEST_MESSAGE_TYPE, \
    GetTrackMetadataRequest
from core.rabbitmq.messages.tracks.track_model import TrackModel
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from yandex.models.track_dto import TrackDto
from yandex.services.yandex_service import YandexMusicService


class GetTrackMetadataRequestHandler(RpcBaseHandler):
    def __init__(self, logger_service: Logger_Service, yandexMusicService: YandexMusicService):
        super().__init__(GET_TRACK_METADATA_REQUEST_MESSAGE_TYPE)
        self.TAG = self.__class__.__name__
        self.logger_service = logger_service
        self.yandexMusicService = yandexMusicService

    def execute(self, payload) -> StatusResponse:
        request = GetTrackMetadataRequest.deserialize(payload)

        search_result: Search = self.yandexMusicService.find_track(request.query)
        track_dto = TrackDto(search_result.best.result)

        cover = search_result.best.result.cover_uri.replace('%%', '1000x1000')

        trackModel = TrackModel(track_dto.title,
                                track_dto.albums,
                                track_dto.artists,
                                track_dto.album_artists,
                                track_dto.year,
                                track_dto.track_position,
                                track_dto.album_tracks,
                                f'https://{cover}')

        return StatusResponse(trackModel.serialize())
