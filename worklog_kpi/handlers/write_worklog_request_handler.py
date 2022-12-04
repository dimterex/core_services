from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.worklog.write_worklog_request import WORKLOG_WRITE_MESSAGE_REQUEST_TYPE, \
    WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from worklog_kpi.write_worklog_action import Write_WorkLok_Action


class Write_Worklog_Request_Handler(RpcBaseHandler):
    def __init__(self, write_WorkLok_Action: Write_WorkLok_Action, logger_service: Logger_Service):
        self.write_WorkLok_Action = write_WorkLok_Action
        self.logger_service = logger_service
        self.TAG = self.__class__.__name__

    def get_message_type(self) -> str:
        return WORKLOG_WRITE_MESSAGE_REQUEST_TYPE

    def execute(self, payload) -> str:
        start_time = convert_rawdate_to_datetime(payload[WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY])
        response = self.write_WorkLok_Action.write(start_time)
        return response.to_json()
