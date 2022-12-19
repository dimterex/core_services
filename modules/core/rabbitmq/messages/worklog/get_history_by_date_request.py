from datetime import datetime

from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_HISTORY_BY_DATE_REQUEST_TYPE = 'get_history_request'
GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY = 'day'


class GetHistoryByDateRequest(BaseMessage):

    def __init__(self, start_day: datetime):
        super().__init__(GET_HISTORY_BY_DATE_REQUEST_TYPE)
        self.start_day = start_day

    def serialize(self) -> dict:
        return self.to_json({
            GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY: str(self.start_day),
        })

