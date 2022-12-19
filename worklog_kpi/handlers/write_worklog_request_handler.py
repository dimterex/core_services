from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.messages.worklog.write_worklog_request import WORKLOG_WRITE_MESSAGE_REQUEST_TYPE, \
    WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from worklog_kpi.write_worklog_action import Write_WorkLok_Action


class Write_Worklog_Request_Handler(RpcBaseHandler):
    def __init__(self, write_WorkLok_Action: Write_WorkLok_Action):
        super().__init__(WORKLOG_WRITE_MESSAGE_REQUEST_TYPE)
        self.write_WorkLok_Action = write_WorkLok_Action

    def execute(self, payload) -> StatusResponse:
        start_time = convert_rawdate_to_datetime(payload[WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY])
        response = self.write_WorkLok_Action.write(start_time)
        return response
