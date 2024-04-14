import os
import warnings

from core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, TRACKS_QUEUE, YANDEX_TOKEN
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from soundcloud.handlers.download_likes_tracks_handler import DownloadLikesTracksHandler
from soundcloud.services.soundcloud_service import SoundCloudService


RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
DOWNLOAD_DIRECTORY_PATH = 'DOWNLOAD_DIRECTORY_PATH'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    download_directory = os.environ[DOWNLOAD_DIRECTORY_PATH]
    rpc_publisher = RpcPublisher(ampq_url)

    soundCloudService = SoundCloudService(download_directory, logger_service)
    download_handler = DownloadLikesTracksHandler(soundCloudService, logger_service, rpc_publisher)
    download_handler.start()
    api_controller = RpcApiController(logger_service)
    rcp = RpcConsumer(ampq_url, TRACKS_QUEUE, api_controller)
    rcp.start()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')

