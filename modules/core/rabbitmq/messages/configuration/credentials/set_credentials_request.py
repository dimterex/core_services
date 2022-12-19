from modules.core.rabbitmq.messages.base_request import BaseMessage
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel

SET_CREDENTIALS_REQUEST_MESSAGE_TYPE = 'set_credentials_request'


class SetCredentialsRequest(BaseMessage):

    def __init__(self, credentialModel: CredentialModel):
        super().__init__(SET_CREDENTIALS_REQUEST_MESSAGE_TYPE)
        self.credentialModel = credentialModel

    def serialize(self):
        return self.to_json(self.credentialModel.serialize())

    @staticmethod
    def deserialize(payload):
        credentialModel = CredentialModel.deserialize(payload)
        return SetCredentialsRequest(credentialModel)
