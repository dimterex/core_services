from core.rabbitmq.messages.configuration.iptv_duplicate_list.get_duplicate_list_request import \
    GetIptvDuplicateListRequest
from core.rabbitmq.messages.configuration.iptv_duplicate_list_item_model import IptvDuplicateListItemModel
from core.rabbitmq.messages.configuration.iptv_epg_source_model import IptvEpgSourceModel
from core.rabbitmq.messages.configuration.iptv_epg_sources.get_iptv_epg_sources_request import GetIptvEpgSourcesRequest
from iptv_filter.services.iptvModificationService import IptvModificationService
from core.helpers.scheduleService import ScheduleService
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.iptv_black_list_item_model import IptvBlackListItemModel
from core.rabbitmq.messages.configuration.iptv_source_model import IptvSourceModel
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from core.rabbitmq.messages.configuration.iptv_black_list.get_black_list_request import GetIptvBlackListRequest
from core.rabbitmq.messages.configuration.iptv_sources.get_iptv_sources_request import GetIptvSourcesRequest


class UpdateService(ScheduleService):
    def __init__(self, logger_Service: Logger_Service, delta: int,
                 rpcPublisher: RpcPublisher,
                 iptvModificationService: IptvModificationService):
        super().__init__(logger_Service, delta)
        self.iptvModificationService = iptvModificationService
        self.rpcPublisher = rpcPublisher

    def update(self):
        black_list_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvBlackListRequest())
        black_list: [IptvBlackListItemModel] = [IptvBlackListItemModel.deserialize(element) for element in black_list_raw.message]

        sources_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvSourcesRequest())
        sources: [str] = [IptvSourceModel.deserialize(element).value for element in sources_raw.message]

        epg_sources_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvEpgSourcesRequest())
        epg_sources: [str] = [IptvEpgSourceModel.deserialize(element).value for element in epg_sources_raw.message]

        duplicate_sources_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvDuplicateListRequest())
        duplicate_sources: [IptvDuplicateListItemModel] = [IptvDuplicateListItemModel.deserialize(element) for element in duplicate_sources_raw.message]
        self.iptvModificationService.run(sources, duplicate_sources, black_list, epg_sources)
