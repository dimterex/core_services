import datetime

from exchangelib import DELEGATE, Credentials, Account, Configuration, EWSDateTime, Task
from exchangelib.protocol import BaseProtocol

import requests.adapters

from modules.models.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.models.outlook_meeting import Outlook_Meeting


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

    def get_meeting(self, start_time: datetime.datetime):
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Connecting to outlook for get meetings...')
        account = Account(self.email, config=self.config, autodiscover=True, access_type=DELEGATE)

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Connected to outlook for get meetings...')
        meetings: list[Outlook_Meeting] = []
        end_time = start_time + datetime.timedelta(days=1)
        for i in account.calendar.view(start=start_time, end=end_time):
            meetings.append(Outlook_Meeting(i))

        account.protocol.close()
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Disconnected to outlook for get meetings...')
        return meetings
