from configuration.database.credentials_table import CredentialsTable
from core.rabbitmq.messages.configuration.credentials.set_credentials_request import SET_CREDENTIALS_REQUEST_MESSAGE_TYPE, SetCredentialsRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class SetCredentialsRequestHandler(RpcBaseHandler):
    def __init__(self, storage: CredentialsTable):
        super().__init__(SET_CREDENTIALS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            setCredentialsRequest = SetCredentialsRequest.deserialize(payload)
            self.storage.set_credentials(setCredentialsRequest.credentialModel)
            return StatusResponse(None)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
