import json

from modules.core.log_service.log_service import Logger_Service, TRACE_LOG_LEVEL, ERROR_LOG_LEVEL
from modules.core.rabbitmq.messages.status_response import StatusResponse, ERROR_STATUS_CODE
from modules.core.rabbitmq.messages.identificators import MESSAGE_TYPE, MESSAGE_PAYLOAD
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class RpcApiController:
    def __init__(self, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.handlers: {str, RpcBaseHandler} = {}
        self.TAG = self.__class__.__name__

    def subscribe(self, handler: RpcBaseHandler):
        type = handler.get_message_type()
        if type not in self.handlers:
            self.handlers[type] = handler

    def received(self, message: str) -> str:
        if message is None:
            return self.send_response(self.generate_exception_response('Message is None'))
        try:
            self.logger_service.send_log(TRACE_LOG_LEVEL, self.TAG, str(message))
            obj = json.loads(message)
            type = obj[MESSAGE_TYPE]
            payload = obj[MESSAGE_PAYLOAD]

            response: StatusResponse = self.handlers[type].execute(payload)

            return self.send_response(response)
        except Exception as e:
            error_message = f'Internal exception. \n Error: {e} \n Message: {message}'
            self.logger_service.send_log(ERROR_LOG_LEVEL, self.TAG, error_message)
            response: StatusResponse = self.generate_exception_response(error_message)
            return self.send_response(response)

    def send_response(self, response: StatusResponse) -> str:
        return json.dumps(response.to_json())

    def generate_exception_response(self, message: str) -> StatusResponse:
        return StatusResponse(message, ERROR_STATUS_CODE)
