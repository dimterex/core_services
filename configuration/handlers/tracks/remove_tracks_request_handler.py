from configuration.database.tracks_table import TracksTable
from core.rabbitmq.messages.configuration.tracks.remove_tracks_request import \
    REMOVE_TRACKS_REQUEST_MESSAGE_TYPE, RemoveTracksRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RemoveTracksRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TracksTable):
        super().__init__(REMOVE_TRACKS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = RemoveTracksRequest.deserialize(payload)
            self.storage.remove(request.ids)
            return StatusResponse("Done")
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
