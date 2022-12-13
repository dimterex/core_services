from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.messages.worklog.get_history_by_date_request import GET_HISTORY_BY_DATE_REQUEST_TYPE, \
    GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler
from worklog_kpi.models.worklog_sqlite_model import WorklogSqliteModel
from worklog_kpi.services.worklog_storage_service import WorklogStorageService


class GetHistoryByDateWorklogRequestHandler(RpcBaseHandler):
    def __init__(self, storage: WorklogStorageService):
        self.storage = storage

    def get_message_type(self) -> str:
        return GET_HISTORY_BY_DATE_REQUEST_TYPE

    def execute(self, payload) -> StatusResponse:
        start_time = convert_rawdate_to_datetime(payload[GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY])
        message: list[WorklogSqliteModel] = self.storage.get_by_date(start_time.date())
        result = []
        for m in message:
            result.append(m.description)

        if len(result) > 1:
            return StatusResponse('\n\n'.join(result))
        else:
            return StatusResponse(result)
