from datetime import datetime

from modules.core.helpers.helper import SECONDS_IN_HOUR, convert_rawdate_with_timezone_to_datetime
from modules.core.log_service.log_service import DEBUG_LOG_LEVEL, Logger_Service
from modules.core.rabbitmq.messages.outlook.get_events_by_date_request import GET_CALENDAR_BY_DATE_REQUEST, \
    GET_CALENDAR_DATE_PROPERTY
from modules.core.rabbitmq.messages.outlook.get_events_by_date_response import GetEventsByDateResponse, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DESCRIPTION_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_LOCATION_PROPERTY
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from modules.models.configuration import Configuration
from outlook.outlook_connection import Outlook_Connection


class GetEventsByDateHandler(RpcBaseHandler):
    def __init__(self, configuration: Configuration, outlook: Outlook_Connection, logger_service: Logger_Service):
        self.configuration = configuration
        self.logger_service = logger_service
        self.outlook = outlook
        self.TAG = self.__class__.__name__

    def get_message_type(self) -> str:
        return GET_CALENDAR_BY_DATE_REQUEST

    def execute(self, payload) -> str:
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Starting modify')
        start_time: datetime = convert_rawdate_with_timezone_to_datetime(payload[GET_CALENDAR_DATE_PROPERTY])
        meetings = self.outlook.get_meeting(start_time)

        worklog = []
        for calendar_item in meetings:
            difference = calendar_item.end - calendar_item.start
            worklog.append({
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY: calendar_item.name,
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY: str(calendar_item.start),
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY: difference.seconds / SECONDS_IN_HOUR,
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY: calendar_item.categories,
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DESCRIPTION_PROPERTY: calendar_item.description,
                GET_CALENDAR_BY_DATE_RESPONSE_EVENT_LOCATION_PROPERTY: calendar_item.location,
            })
        response = GetEventsByDateResponse(worklog).to_json()
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Ending modify')
        return response
