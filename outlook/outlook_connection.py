import datetime

from exchangelib import DELEGATE, Credentials, Account, Configuration
from exchangelib.protocol import BaseProtocol

import requests.adapters

from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from core.rabbitmq.messages.outlook.outlook_meeting import Outlook_Meeting


class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn=conn, url=url, verify={}, cert=cert)


# # Tell exchangelib to use this adapter class instead of the default
BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter


class Outlook_Connection:
    def __init__(self, url: str, user: str, credentialModel: CredentialModel, logger_service: Logger_Service):
        self.credentialModel = credentialModel
        self.logger_service = logger_service
        credentials = Credentials(username=user, password=self.credentialModel.password)
        self.config = Configuration(server=url, credentials=credentials, auth_type=None)
        self.TAG = self.__class__.__name__

    def get_meeting(self, start_time: datetime.datetime) -> list[Outlook_Meeting]:
        self.logger_service.debug(self.TAG, 'Connecting to outlook for get meetings...')
        meetings: list[Outlook_Meeting] = []
        try:
            account = Account(self.credentialModel.email, config=self.config, access_type=DELEGATE)
            self.logger_service.debug(self.TAG, 'Connected to outlook for get meetings...')

            end_time = start_time + datetime.timedelta(days=1)
            for i in account.calendar.view(start=start_time, end=end_time):
                meetings.append(Outlook_Meeting(i))

            account.protocol.close()
            self.logger_service.debug(self.TAG, 'Disconnected to outlook for get meetings...')
        except Exception as e:
            self.logger_service.error(self.TAG, f'{e}')

        return meetings
