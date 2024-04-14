from core.helpers.scheduleService import ScheduleService
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from core.rabbitmq.messages.configuration.tracks.add_new_track_request import AddNewTrackRequest
from core.rabbitmq.messages.configuration.tracks.get_track_by_id_request import GetTrackRequest, \
    SOUNDCLOUD_SOURCE
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, SOUNDCLOUD_CLIENT_ID, SOUNDCLOUD_USER_ID
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from soundcloud.models.track_dto import TrackDto
from soundcloud.services.soundcloud_service import SoundCloudService


class DownloadLikesTracksHandler(ScheduleService):
    def __init__(self, soundCloudService: SoundCloudService, logger_Service: Logger_Service, rpcPublisher: RpcPublisher):
        super().__init__(logger_Service, 12)
        self.rpcPublisher = rpcPublisher
        self.logger_Service = logger_Service
        self.soundCloudService = soundCloudService

    def update(self):

        soundcloud_client_id_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTokenRequest(SOUNDCLOUD_CLIENT_ID))

        if soundcloud_client_id_response.status == ERROR_STATUS_CODE:
            raise Exception(soundcloud_client_id_response.message)

        soundcloud_user_id_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTokenRequest(SOUNDCLOUD_USER_ID))

        if soundcloud_user_id_response.status == ERROR_STATUS_CODE:
            raise Exception(soundcloud_user_id_response.message)

        tracks: list[TrackDto] = self.soundCloudService.get_songs(soundcloud_client_id_response.message, soundcloud_user_id_response.message)
        for track in tracks:
            track_model_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetTrackRequest(track.id, SOUNDCLOUD_SOURCE))

            if track_model_response.status == ERROR_STATUS_CODE:
                track_name = self.soundCloudService.download(track)
                add_track_model_response = self.rpcPublisher.call(CONFIGURATION_QUEUE, AddNewTrackRequest(track.id, track_name, SOUNDCLOUD_SOURCE))
                if add_track_model_response.status == ERROR_STATUS_CODE:
                    raise Exception(add_track_model_response.message)
