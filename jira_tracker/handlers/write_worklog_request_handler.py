import json

from jira_tracker.jira_connection import Jira_Connection
from modules.core.helpers.helper import convert_rawdate_with_timezone_to_datetime
from modules.core.rabbitmq.messages.jira_tracker.write_worklog_request import WRITE_WORKLOG_REQUEST_WORKLOGS, \
    WRITE_WORKLOG_REQUEST_MESSAGE_TYPE
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.core.rabbitmq.messages.status_response import StatusResponse, ERROR_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class WriteWorklogRequestHandler(RpcBaseHandler):
    def __init__(self, jira: Jira_Connection, logger_service: Logger_Service):
        super().__init__(WRITE_WORKLOG_REQUEST_MESSAGE_TYPE)
        self.logger_service = logger_service
        self.jira = jira
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        worklogs = payload[WRITE_WORKLOG_REQUEST_WORKLOGS]
        self.logger_service.debug(self.TAG, 'Connecting to jira for write worklogs...')
        try:
            jira = self.jira.connect_to_jira()
            self.logger_service.debug(self.TAG, 'Connected to jira for write worklogs...')

            for issue in worklogs:
                name = issue['name']
                date = convert_rawdate_with_timezone_to_datetime(issue['date'])
                tracker_id = issue['tracker_id']
                duration = issue['duration']
                jira.add_worklog(tracker_id, timeSpent=f'{duration}', started=date, comment=name)

            jira.close()
            response = StatusResponse(None)
            self.logger_service.debug(self.TAG, 'Disconnected to jira for write worklogs...')
        except Exception as e:
            response = StatusResponse(f'{e}', ERROR_STATUS_CODE)

        return response
