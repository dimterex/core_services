from datetime import datetime

from modules.core.helpers.helper import SECONDS_IN_HOUR, convert_rawdate_with_timezone_to_datetime
from modules.core.log_service.log_service import DEBUG_LOG_LEVEL, Logger_Service
from modules.core.rabbitmq.messages.outlook.get_events_by_date_request import GET_CALENDAR_BY_DATE_REQUEST, \
    GET_CALENDAR_DATE_PROPERTY
from modules.core.rabbitmq.messages.status_response import StatusResponse

from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from modules.models.configuration import Configuration
from outlook.models.outlook_meeting import Outlook_Meeting
from outlook.outlook_connection import Outlook_Connection


class GetEventsByDateHandler(RpcBaseHandler):
    def __init__(self, configuration: Configuration, outlook: Outlook_Connection, logger_service: Logger_Service):
        self.configuration = configuration
        self.logger_service = logger_service
        self.outlook = outlook
        self.TAG = self.__class__.__name__

    def get_message_type(self) -> str:
        return GET_CALENDAR_BY_DATE_REQUEST

    def execute(self, payload) -> StatusResponse:
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Starting modify')
        start_time: datetime = convert_rawdate_with_timezone_to_datetime(payload[GET_CALENDAR_DATE_PROPERTY])
        meetings: list[Outlook_Meeting] = self.outlook.get_meeting(start_time)

        worklogs = []
        for calendar_item in meetings:
            worklogs.append(calendar_item.to_json())
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Ending modify')
        response = StatusResponse(worklogs)
        return response
