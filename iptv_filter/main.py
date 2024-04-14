import os
import warnings

from iptv_filter.services.iptvModificationService import IptvModificationService
from iptv_filter.services.updateService import UpdateService

from core.rabbitmq.messages.identificators import IPTV_QUEUE
from core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
IPTV_PLAYLIST_PATH = 'IPTV_PLAYLIST_PATH'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    iptv_playlist_path = os.environ[IPTV_PLAYLIST_PATH]
    rpc_publisher = RpcPublisher(ampq_url)

    iptvModificationService = IptvModificationService(logger_service, iptv_playlist_path)

    updateService = UpdateService(logger_service, 12, rpc_publisher, iptvModificationService)
    updateService.run()

    api_controller = RpcApiController(logger_service)
    rcp = RpcConsumer(ampq_url, IPTV_QUEUE, api_controller)
    rcp.start()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')
