import sys
import os
import time
import warnings
import socket

from datetime import datetime, timezone

from todoist_api_python.api import TodoistAPI

from modules.connections.jira_connection import Jira_Connection
from modules.connections.outlook_connection import Outlook_Connection
from modules.rabbitmq.messages.api_controller import Api_Controller
from modules.rabbitmq.messages.discord.send_message import Send_Message
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE, WORKLOG_QUEUE, WORKLOG_WRITE_MESSAGE
from modules.rabbitmq.publisher import Publisher
from modules.rabbitmq.receive import Consumer
from modules.worklog_core.meetings_writer import Worklog_by_Meetings
from modules.models.configuration import Configuration
from modules.worklog_core.services.worklog_service import Worklog_Service
from modules.worklog_core.worklog_periodical import Worklog_By_Periodical
from modules.worklog_core.worklog_tasks_v2 import Worklog_By_Tasks_v2
from modules.worklog_core.write_worklog_action import Write_WorkLok_Action

SETTINGS_FILE = 'settings.json'
HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'
TODOIST_API_TOKEN = 'TODOIST_API_TOKEN'


def convert_rawdate_to_datetime(raw_date: str):
    # convert from string format to datetime format
    return datetime.strptime(raw_date, '%Y/%m/%d')


def main():
    host = socket.gethostbyname(os.environ[HOST_ENVIRON])
    raw_port = os.environ[PORT_ENVIRON]
    todoistToken = os.environ[TODOIST_API_TOKEN]
    port = int(raw_port)

    api_controller = Api_Controller()
    publisher = Publisher(host, port)
    consumer = Consumer(host, port, WORKLOG_QUEUE, api_controller)

    configuration = None
    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        configuration = Configuration(raw_data)

    jira_connection = Jira_Connection(configuration.jira, configuration.login, configuration.password)
    domain_login = f'{configuration.domain}\\{configuration.login}'
    outlook_connection = Outlook_Connection(configuration.outlook, configuration.email, domain_login, configuration.password)
    todoistApi = TodoistAPI(todoistToken)

    write_WorkLok_Action = Write_WorkLok_Action(configuration, jira_connection, todoistApi, outlook_connection, publisher)

    def write_worklog_action(obj):
        promise_id = obj['promise_id']
        start_time = convert_rawdate_to_datetime(obj['start_day'])
        write_WorkLok_Action.write(promise_id, start_time)

    api_controller.configure(WORKLOG_QUEUE, WORKLOG_WRITE_MESSAGE, write_worklog_action)

    consumer.start()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')
    try:
        while True:
            time.sleep(1)
    finally:
        pass

