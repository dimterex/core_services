from datetime import datetime

from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_CALENDAR_BY_DATE_REQUEST = 'get_calendar_by_date_request'
GET_CALENDAR_DATE_PROPERTY = 'date'


class GetEventsByDateRequest(BaseMessage):
    def __init__(self, date: datetime):
        super().__init__(GET_CALENDAR_BY_DATE_REQUEST)
        self.date = str(date)

    def serialize(self) -> dict:
        return self.to_json({
            GET_CALENDAR_DATE_PROPERTY: self.date,
        })
