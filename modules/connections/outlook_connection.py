import datetime

from exchangelib import DELEGATE, Credentials, Account, Configuration, EWSDateTime, Task
from exchangelib.protocol import BaseProtocol

import requests.adapters

from modules.models.outlook_meeting import Outlook_Meeting
from modules.models.outlook_task import Outlook_Task, ALL_TIME_TO_TASK, JIRA_ISSUE_ID


class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn=conn, url=url, verify={}, cert=cert)


# # Tell exchangelib to use this adapter class instead of the default
BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter


class Outlook_Connection:
    def __init__(self, url: str, email: str, user: str, passwrd: str):
        self.email = email
        credentials = Credentials(username=user, password=passwrd)
        self.config = Configuration(server=url, credentials=credentials, auth_type=None)

    def get_meeting(self, start_time: datetime.datetime, end_time: datetime.datetime):
        print('Connecting to outlook for get meetings...')
        account = Account(self.email, config=self.config, autodiscover=True, access_type=DELEGATE)

        print('Connected to outlook for get meetings...')
        meetings: list[Outlook_Meeting] = []
        for i in account.calendar.view(start=start_time, end=end_time):
            meetings.append(Outlook_Meeting(i))

        account.protocol.close()
        print('Disconnected to outlook for get meetings...')
        return meetings

    def get_tasks(self, start_time: datetime.datetime, end_time: datetime.datetime):
        print('Connecting to outlook for get tasks...')
        tasks: list[Outlook_Task] = []
        start_date = EWSDateTime.from_datetime(start_time).date()
        end_date = EWSDateTime.from_datetime(end_time).date()
        account = Account(self.email, config=self.config, autodiscover=True, access_type=DELEGATE)
        print('Connected to outlook for get tasks...')
        for task_item in account.tasks.all():
            if task_item.start_date is None:
                continue

            if task_item.is_complete:
                continue

            if task_item.start_date < start_date:
                continue

            if task_item.start_date > end_date:
                continue

            tasks.append(Outlook_Task(task_item))

        account.protocol.close()
        print('Disconnected to outlook for get tasks...')
        return tasks

    def create_task(self, name: str, start_date: datetime.datetime, duration: float, issue_id: str):
        print('Connecting to outlook for creating task...')
        tasks = []
        task_item = Task()

        task_item.start_date = EWSDateTime.from_datetime(start_date).date()
        new_name = []
        new_name.append(name)
        if duration > 0:
            new_name.append(f'{ALL_TIME_TO_TASK}{duration}')
        new_name.append(f'{JIRA_ISSUE_ID}{issue_id}')

        task_item.subject = ';'.join(new_name)
        tasks.append(task_item)
        account = Account(self.email, config=self.config, autodiscover=True, access_type=DELEGATE)
        print('Connected to outlook for creating task...')
        account.bulk_create(folder=account.tasks, items=tasks)
        account.protocol.close()
        print('Disconnected to outlook for creating task...')
