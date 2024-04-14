from iptv_filter.services.iptvModificationService import IptvModificationService
from core.helpers.scheduleService import ScheduleService
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.iptv_black_list_item_model import IptvBlackListItemModel, CHANNEL_TYPE, CATEGORY_TYPE
from core.rabbitmq.messages.configuration.iptv_source_model import IptvSourceModel
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from core.rabbitmq.messages.configuration.iptv_black_list.get_black_list_request import GetIptvBlackListRequest
from core.rabbitmq.messages.configuration.iptv_sources.get_iptv_sources_request import GetIptvSourcesRequest


class UpdateService(ScheduleService):
    def __init__(self, logger_Service: Logger_Service, delta: int, rpcPublisher: RpcPublisher, iptvModificationService: IptvModificationService):
        super().__init__(logger_Service, delta)
        self.iptvModificationService = iptvModificationService
        self.rpcPublisher = rpcPublisher

    def update(self):
        black_list_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvBlackListRequest())
        sources_raw = self.rpcPublisher.call(CONFIGURATION_QUEUE, GetIptvSourcesRequest())
        black_list: [IptvBlackListItemModel] = [IptvBlackListItemModel.deserialize(element) for element in black_list_raw.message]
        sources: [str] = [IptvSourceModel.deserialize(element).value for element in sources_raw.message]

        channel_black_list = [element.value for element in black_list if element.type == CHANNEL_TYPE]
        category_black_list = [element.value for element in black_list if element.type == CATEGORY_TYPE]

        self.iptvModificationService.parse(sources, channel_black_list, category_black_list)
