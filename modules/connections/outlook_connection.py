from exchangelib import DELEGATE, Credentials, Account, Configuration, EWSDateTime
from exchangelib.protocol import BaseProtocol

import requests.adapters

from modules.models.outlook_task import Outlook_Task


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

    def get_tasks(self, start_time, end_time):
        tasks = []
        start_date = EWSDateTime.from_datetime(start_time).date()
        end_date = EWSDateTime.from_datetime(end_time).date()

        for task_item in self.account.tasks.all():
            if task_item.start_date is None:
                continue

            if task_item.is_complete:
                continue

            if task_item.start_date < start_date:
                continue

            if task_item.start_date > end_date:
                continue

            task = Outlook_Task(task_item)
            tasks.append(task)
        return tasks
