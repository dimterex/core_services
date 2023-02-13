from modules.core.rabbitmq.messages.base_request import BaseMessage

WRITE_WORKLOG_REQUEST_MESSAGE_TYPE = 'write_worklog_request'
WRITE_WORKLOG_REQUEST_WORKLOGS = 'worklogs'


class WriteWorklogsRequest(BaseMessage):

    def __init__(self, worklogs: []):
        super().__init__(WRITE_WORKLOG_REQUEST_MESSAGE_TYPE)
        self.worklogs = worklogs

    def serialize(self) -> dict:
        return self.to_json({
            WRITE_WORKLOG_REQUEST_WORKLOGS: self.worklogs,
        })

    @staticmethod
    def deserialize(payload):
        worklogs = payload[WRITE_WORKLOG_REQUEST_WORKLOGS]
        return WriteWorklogsRequest(worklogs)
