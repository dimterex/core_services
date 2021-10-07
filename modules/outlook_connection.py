from exchangelib import DELEGATE, Credentials, Account, Configuration
from exchangelib.protocol import BaseProtocol

from urllib.parse import urlparse

import requests.adapters
import datetime

class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """
    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn=conn, url=url, verify={}, cert=cert)

# # Tell exchangelib to use this adapter class instead of the default
BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter


class Outlook_Connection:
    def __init__(self, url, email, user, passwrd):
        credentials = Credentials(username=user, password=passwrd)
        config = Configuration(server=url, credentials=credentials, auth_type=None)

        self.account = Account(email, config=config, autodiscover=True, access_type=DELEGATE)


    def get_meeting(self, start_time, end_time):
        meetings = []
        for i in self.account.calendar.view(start=start_time, end=end_time):
            meetings.append(i)
        return meetings
