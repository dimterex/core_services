from datetime import datetime

from core.helpers.helper import convert_rawdate_with_timezone_to_datetime
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.outlook.get_events_by_date_request import GET_CALENDAR_BY_DATE_REQUEST, \
    GET_CALENDAR_DATE_PROPERTY
from core.rabbitmq.messages.status_response import StatusResponse
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from core.rabbitmq.messages.outlook.outlook_meeting import Outlook_Meeting
from outlook.outlook_connection import Outlook_Connection


class GetEventsByDateHandler(RpcBaseHandler):
    def __init__(self, outlook: Outlook_Connection, logger_service: Logger_Service):
        super().__init__(GET_CALENDAR_BY_DATE_REQUEST)
        self.logger_service = logger_service
        self.outlook = outlook
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        self.logger_service.debug(self.TAG, 'Starting modify')
        start_time: datetime = convert_rawdate_with_timezone_to_datetime(payload[GET_CALENDAR_DATE_PROPERTY])
        meetings: list[Outlook_Meeting] = self.outlook.get_meeting(start_time)

        worklogs = []
        for calendar_item in meetings:
            worklogs.append(calendar_item.serialize())
        self.logger_service.debug(self.TAG, 'Ending modify')
        response = StatusResponse(worklogs)
        return response
