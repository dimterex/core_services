from configuration.database.credentials_table import CredentialsTable
from modules.core.rabbitmq.messages.configuration.credentials.get_credentials_request import GET_CREDENTIALS_REQUEST_MESSAGE_TYPE
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetCredentialsRequestHandler(RpcBaseHandler):
    def __init__(self, storage: CredentialsTable):
        super().__init__(GET_CREDENTIALS_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            return StatusResponse(self.storage.get_credentials().serialize())
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
