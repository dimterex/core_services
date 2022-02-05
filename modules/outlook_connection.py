from exchangelib import DELEGATE, Credentials, Account, Configuration, EWSDateTime
from exchangelib.protocol import BaseProtocol

import requests.adapters


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
            # print(f'\n {task_item.subject}')
            # print('\t {} {}'.format('datetime_received', task_item.datetime_received))
            # print('\t {} {}'.format('datetime_sent', task_item.datetime_sent))
            # print('\t {} {}'.format('datetime_created', task_item.datetime_created))
            # print('\t {} {}'.format('due_date', task_item.due_date))
            # print('\t {} {}'.format('is_complete', task_item.is_complete))
            # print('\t {} {}'.format('start_date', task_item.start_date))
            # print('\t {} {}'.format('status', task_item.status))

            if task_item.start_date is None:
                # print('{} \n'.format('not start_date '))
                continue

            if task_item.is_complete:
                # print('\t is complited.')
                continue

            if task_item.start_date < start_date:
                # print('\t {} {}'.format('start_date ', task_item.subject))
                continue

            if task_item.start_date > end_date:
                # print('\t {} {}'.format('end_date ', task_item.subject))
                continue
            tasks.append(task_item)
            # print('\t selected')
            # print('{} {}'.format('subject', task_item.subject))
            # print('{} {}'.format('text_body', task_item.text_body))
            # print('{} {}'.format('datetime_received', task_item.datetime_received))
            # print('{} {}'.format('categories', task_item.categories))
            # print('{} {}'.format('datetime_sent', task_item.datetime_sent))
            # print('{} {}'.format('datetime_created', task_item.datetime_created))
            # print('{} {}'.format('due_date', task_item.due_date))
            # print('{} {}'.format('is_complete', task_item.is_complete))
            # print('{} {}'.format('start_date', task_item.start_date))
            # print('{} {} \n'.format('status', task_item.status))

        return tasks
