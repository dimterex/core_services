import datetime

from exchangelib import DELEGATE, Credentials, Account, Configuration
from exchangelib.protocol import BaseProtocol

import requests.adapters

from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL, ERROR_LOG_LEVEL
from outlook.models.outlook_meeting import Outlook_Meeting


class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn=conn, url=url, verify={}, cert=cert)


# # Tell exchangelib to use this adapter class instead of the default
BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter


class Outlook_Connection:
    def __init__(self, url: str, email: str, user: str, passwrd: str, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.email = email
        credentials = Credentials(username=user, password=passwrd)
        self.config = Configuration(server=url, credentials=credentials, auth_type=None)
        self.TAG = self.__class__.__name__

    def get_meeting(self, start_time: datetime.datetime) -> list[Outlook_Meeting]:
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Connecting to outlook for get meetings...')
        meetings: list[Outlook_Meeting] = []
        try:
            account = Account(self.email, config=self.config, access_type=DELEGATE)
            self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Connected to outlook for get meetings...')

            end_time = start_time + datetime.timedelta(days=1)
            for i in account.calendar.view(start=start_time, end=end_time):
                meetings.append(Outlook_Meeting(i))

            account.protocol.close()
            self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Disconnected to outlook for get meetings...')
        except Exception as e:
            self.logger_service.send_log(ERROR_LOG_LEVEL, self.TAG, f'{e}')

        return meetings
