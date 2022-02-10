import sys
import os
import warnings
from datetime import datetime

from tzlocal import get_localzone

from modules.connections.jira_connection import Jira_Connection
from modules.connections.outlook_connection import Outlook_Connection
from modules.rabbitmq.messages.api_controller import Api_Controller
from modules.rabbitmq.messages.discord.send_message import Send_Message
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE, WORKLOG_QUEUE, WORKLOG_WRITE_MESSAGE
from modules.rabbitmq.publisher import Publisher
from modules.rabbitmq.receive import Consumer
from modules.worklog_core.meetings_writer import Worklog_by_Meetings
from modules.models.Configuration import Config
from modules.worklog_core.services.worklog_service import Worklog_Service
from modules.worklog_core.worklog_periodical import Worklog_By_Periodical
from modules.worklog_core.worklog_tasks import Worklog_By_Tasks

SETTINGS_FILE = 'settings.json'

def convert_rawdate_to_datetime(raw_date):
    # convert from string format to datetime format
    return datetime.strptime(raw_date, '%Y/%m/%d')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    try:
        host = "dimterex.duckdns.org"
        port = 56789

        api_controller = Api_Controller()
        publisher = Publisher(host, port)
        consumer = Consumer(host, port, WORKLOG_QUEUE, api_controller)

        with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
            raw_data = json_file.read()
            сonfiguration = Config(raw_data)

        local_tz = get_localzone()

        jira_connection = Jira_Connection(сonfiguration.jira, сonfiguration.login, сonfiguration.password)
        domain_login = f'{сonfiguration.domain}\\{сonfiguration.login}'
        outlook_connection = Outlook_Connection(сonfiguration.outlook, сonfiguration.email, domain_login, сonfiguration.password)

        def write_worklog_action(obj):
            promise_id = obj['promise_id']
            start_time = convert_rawdate_to_datetime(obj['start_day'])
            end_time = convert_rawdate_to_datetime(obj['end_date'])

            start_time = start_time.replace(tzinfo=local_tz)
            end_time = end_time.replace(tzinfo=local_tz)

            worklogs_service = Worklog_Service()
            Worklog_by_Meetings(сonfiguration, start_time, end_time, jira_connection, outlook_connection, worklogs_service).modify()
            Worklog_By_Periodical(сonfiguration, start_time, end_time, worklogs_service).modify()
            Worklog_By_Tasks(сonfiguration, start_time, end_time, jira_connection, outlook_connection, worklogs_service).modify()

            by_dates = worklogs_service.get_by_dates()
            message = []
            for date in by_dates:
                timelog = worklogs_service.get_summary_by_date(date)
                message.append(f'Day: {date}')
                print(f'Day: {date}')
                for worklog in by_dates[date]:
                    message.append(f'\t {worklog.duration} | {worklog.issue_id} | {worklog.name}')
                    print(f'\t {worklog.duration} | {worklog.issue_id} | {worklog.name}')

                print(f'\t Summary: {timelog}')
                message.append(f'\t Summary: {timelog}')

            # TODO: Писать в джиру.
            # jira_connection.write_worklogs(worklogs_service.worklogs)
            publisher.send_message(DISCORD_QUEUE, Send_Message(promise_id, '\n'.join(message)).to_json())

        api_controller.configure(WORKLOG_QUEUE, WORKLOG_WRITE_MESSAGE, write_worklog_action)

        consumer.start()

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
