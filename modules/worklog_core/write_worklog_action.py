import asyncio
import datetime
import threading

from todoist_api_python.api import TodoistAPI

from modules.connections.jira_connection import Jira_Connection
from modules.connections.outlook_connection import Outlook_Connection
from modules.models.configuration import Configuration
from modules.models.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.rabbitmq.messages.discord.send_message import Send_Message
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE
from modules.rabbitmq.publisher import Publisher
from modules.worklog_core.meetings_writer import Worklog_by_Meetings
from modules.worklog_core.services.worklog_service import Worklog_Service
from modules.worklog_core.worklog_periodical import Worklog_By_Periodical
from modules.worklog_core.worklog_tasks_v2 import Worklog_By_Tasks_v2


class Write_WorkLok_Action:
    def __init__(self, 
                 configuration: Configuration,
                 issue_tracker: Jira_Connection,
                 todoistAPI: TodoistAPI,
                 outlook: Outlook_Connection,
                 publisher: Publisher,
                 logger_service: Logger_Service):
        self.logger_service = logger_service
        self.publisher = publisher
        self.todoistAPI = todoistAPI
        self.configuration = configuration
        self.issue_tracker = issue_tracker
        self.outlook = outlook
    
    def write(self, promise_id: str, start_time: datetime.datetime):
        self.write_sync(promise_id, start_time)

    def write_sync(self, promise_id: str, start_time: datetime.datetime):
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Starting modify')
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)

        worklogs_service = Worklog_Service()
        Worklog_by_Meetings(self.configuration, start_time, self.issue_tracker, self.outlook, worklogs_service, self.logger_service).modify()
        Worklog_By_Periodical(self.configuration, start_time, worklogs_service, self.logger_service).modify()
        Worklog_By_Tasks_v2(self.configuration, start_time, self.issue_tracker, self.todoistAPI, worklogs_service, self.logger_service).modify()

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Prepare tasks ...')
        message: list[str] = []
        timelog = worklogs_service.get_summary()
        message.append(f'Day: {start_time}')
        for worklog in worklogs_service.worklogs:
            url = f'{self.configuration.jira}/browse/{worklog.issue_id}'
            message.append(f'\t {worklog.duration} | {url} | {worklog.name}')

        message.append(f'\t Summary: {timelog}')

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Send result message')
        self.publisher.send_message(DISCORD_QUEUE, Send_Message(promise_id, '\n'.join(message)).to_json())

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Write worklog')
        self.issue_tracker.write_worklogs(worklogs_service.worklogs)

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Ended')
