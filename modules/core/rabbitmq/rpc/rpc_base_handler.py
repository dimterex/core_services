from modules.core.rabbitmq.messages.status_response import StatusResponse


class RpcBaseHandler:
    def get_message_type(self) -> str:
        raise Exception('Not implemented')

    def execute(self, payload) -> StatusResponse:
        raise Exception('Not implemented')
