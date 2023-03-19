from configuration.database.tracks_table import TracksTable
from modules.core.rabbitmq.messages.configuration.tracks.get_tracks_request import GET_TRACKS_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetTracksRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TracksTable):
        super().__init__(GET_TRACKS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            tracks = self.storage.get_tracks()
            response = []
            for track in tracks:
                response.append(track.serialize())
            return StatusResponse(response)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
