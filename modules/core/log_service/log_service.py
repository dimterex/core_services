from datetime import datetime

from modules.core.rabbitmq.messages.logger.log_message import Log_Message

TRACE_LOG_LEVEL = 'Trace'
DEBUG_LOG_LEVEL = 'Debug'
INFO_LOG_LEVEL = 'Info'
WARNING_LOG_LEVEL = 'Warning'
ERROR_LOG_LEVEL = 'Error'


class Logger_Service:
    def __init__(self, application_name: str):
        self.application_name = application_name
        self.action = None

    def configure_action(self, action):
        self.action = action

    def send_log(self, level: str, tag: str, message: str):
        if self.action is None:
            print(f'{level}\t{tag}\t{message}')
            return
        log_message = Log_Message(self.application_name, tag, level, f'{datetime.now()}', message)
        self.action(log_message)
