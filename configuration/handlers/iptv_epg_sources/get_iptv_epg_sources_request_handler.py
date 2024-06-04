from configuration.database.iptv_epg_sources_table import IptvEpgSourcesTable
from core.rabbitmq.messages.configuration.iptv_epg_sources.get_iptv_epg_sources_request import \
    GET_IPTV_EPG_SOURCES_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetIptvEpgSourcesRequestHandler(RpcBaseHandler, Logger_Service):
    def __init__(self, storage: IptvEpgSourcesTable):
        super().__init__(GET_IPTV_EPG_SOURCES_REQUEST_MESSAGE_TYPE)
        self.storage = storage

    def execute(self, payload) -> StatusResponse:
        try:
            data = self.storage.get_sources()
            response = []
            for source in data:
                response.append(source.serialize())
            return StatusResponse(response)
        except Exception as e:
            return StatusResponse(e, ERROR_STATUS_CODE)
