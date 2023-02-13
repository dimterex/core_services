from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_STATISTICS_REQUEST_MESSAGE_TYPE = 'get_statistics_request'
GET_STATISTICS_REQUEST_YEAR = 'year'
GET_STATISTICS_REQUEST_MONTH = 'month'


class GetStatisticsRequest(BaseMessage):

    def __init__(self, year: int, month: int):
        super().__init__(GET_STATISTICS_REQUEST_MESSAGE_TYPE)
        self.year = year
        self.month = month

    def serialize(self) -> dict:
        return self.to_json({
            GET_STATISTICS_REQUEST_YEAR: self.year,
            GET_STATISTICS_REQUEST_MONTH: self.month,
        })

    @staticmethod
    def deserialize(payload):
        year = payload[GET_STATISTICS_REQUEST_YEAR]
        month = payload[GET_STATISTICS_REQUEST_MONTH]
        return GetStatisticsRequest(year, month)
