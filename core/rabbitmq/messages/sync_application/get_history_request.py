
from core.rabbitmq.messages.base_request import BaseMessage

GET_SYNC_HISTORY_REQUEST_MESSAGE_TYPE = 'get_history_request'


class GetSyncHistoryRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_SYNC_HISTORY_REQUEST_MESSAGE_TYPE)

    def serialize(self) -> dict:
        return self.to_json({ })
