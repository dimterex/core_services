from core.rabbitmq.messages.status_response import StatusResponse


class RpcBaseHandler:
    def __init__(self, message_type: str):
        self.message_type = message_type
        self.TAG = self.__class__.__name__

    def execute(self, payload: dict) -> StatusResponse:
        raise Exception('Not implemented')
