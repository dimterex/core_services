from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from web_host.messages.base_response import BaseResponse


class CredentialsResponse(BaseResponse):
    def __init__(self, status: str, credentials: CredentialModel= None, exception: str = None):
        super().__init__(status, exception)
        self.credentials = credentials
        self.exception = exception
        self.status = status

    def toJson(self) -> dict:
        return {
            'status': self.status,
            'credentials': self.credentials,
            'exception': self.exception,
        }
