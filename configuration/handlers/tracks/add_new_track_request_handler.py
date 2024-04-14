from configuration.database.tracks_table import TracksTable
from core.rabbitmq.messages.configuration.tracks.add_new_track_request import \
    ADD_NEW_TRACK_REQUEST_MESSAGE_TYPE, AddNewTrackRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class AddNewTrackRequestHandler(RpcBaseHandler):
    def __init__(self, storage: TracksTable):
        super().__init__(ADD_NEW_TRACK_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            request = AddNewTrackRequest.deserialize(payload)
            new_id = self.storage.add_new_track(request.track_id, request.name, request.source)
            return StatusResponse(new_id)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
