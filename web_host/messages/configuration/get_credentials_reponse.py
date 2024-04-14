from core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from core.http_server.base_response import BaseResponse


class CredentialsResponse(BaseResponse):
    def __init__(self, status: str, credentials: CredentialModel= None, exception: str = None):
        super().__init__(status, exception)
        self.credentials = credentials

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'credentials': self.credentials,
            'exception': self.exception,
        }
