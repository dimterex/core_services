from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_WORKLOGS_REQUEST_MESSAGE_TYPE = 'get_worklogs_request'
GET_WORKLOGS_REQUEST_YEAR = 'year'
GET_WORKLOGS_REQUEST_MONTH = 'month'


class GetWorklogsRequest(BaseMessage):

    def __init__(self, year: int, month: int):
        super().__init__(GET_WORKLOGS_REQUEST_MESSAGE_TYPE)
        self.year = year
        self.month = month

    def serialize(self) -> dict:
        return self.to_json({
            GET_WORKLOGS_REQUEST_YEAR: self.year,
            GET_WORKLOGS_REQUEST_MONTH: self.month,
        })

    @staticmethod
    def deserialize(payload):
        year = payload[GET_WORKLOGS_REQUEST_YEAR]
        month = payload[GET_WORKLOGS_REQUEST_MONTH]
        return GetWorklogsRequest(year, month)
