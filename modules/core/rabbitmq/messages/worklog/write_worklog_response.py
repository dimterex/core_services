from modules.core.rabbitmq.messages.base_request import BaseMessage

WORKLOG_WRITE_MESSAGE_RESPONSE_TYPE = 'write_worklog_response'
WORKLOG_WRITE_MESSAGE_RESPONSE_RESULT_PROPERTY = 'result'


class Write_Worklog_Response(BaseMessage):

    def __init__(self, result: str):
        super().__init__(WORKLOG_WRITE_MESSAGE_RESPONSE_TYPE)
        self.result = result

    def serialize(self) -> dict:
        return self.to_json({
            WORKLOG_WRITE_MESSAGE_RESPONSE_RESULT_PROPERTY: str(self.result),
        })
