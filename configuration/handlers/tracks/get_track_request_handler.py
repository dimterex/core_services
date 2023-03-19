from configuration.database.tracks_table import TracksTable
from modules.core.rabbitmq.messages.configuration.tracks.get_track_by_id_request import GET_TRACK_REQUEST_MESSAGE_TYPE, \
    GetTrackRequest
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetTrackRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TracksTable):
        super().__init__(GET_TRACK_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = GetTrackRequest.deserialize(payload)
            track = self.storage.get_track_by_track_id(request.track_id)
            return StatusResponse(track.serialize())
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
