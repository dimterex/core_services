import datetime

from core.rabbitmq.messages.base_request import BaseMessage

WORKLOG_WRITE_MESSAGE_REQUEST_TYPE = 'write_worklog_request'
WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY = 'start_day'


class Write_Worklog_Request(BaseMessage):

    def __init__(self, start_day: datetime.datetime):
        super().__init__(WORKLOG_WRITE_MESSAGE_REQUEST_TYPE)
        self.start_day = start_day

    def serialize(self) -> dict:
        return self.to_json({
            WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY: str(self.start_day),
        })
