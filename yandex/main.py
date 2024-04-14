import os
import warnings

from core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, TRACKS_QUEUE, YANDEX_TOKEN
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from core.log_service.log_service import Logger_Service
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from yandex.handlers.download_likes_tracks_handler import DownloadLikesTracksHandler
from yandex.handlers.get_track_metadata_request_handler import GetTrackMetadataRequestHandler
from yandex.services.tags_service import TagsService
from yandex.services.yandex_service import YandexMusicService

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
DOWNLOAD_DIRECTORY_PATH = '/downloads'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    rpc_publisher = RpcPublisher(ampq_url)

    token_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(YANDEX_TOKEN))

    if token_response.status == ERROR_STATUS_CODE:
        raise Exception(token_response.message)
    yandexService = YandexMusicService(str(token_response.message), DOWNLOAD_DIRECTORY_PATH, logger_service)
    trackService = TagsService(logger_service)

    download_handler = DownloadLikesTracksHandler(yandexService, trackService, logger_service, rpc_publisher)
    download_handler.start()
    api_controller = RpcApiController(logger_service)
    rcp = RpcConsumer(ampq_url, TRACKS_QUEUE, api_controller)
    api_controller.subscribe(GetTrackMetadataRequestHandler(logger_service, yandexService))
    rcp.start()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')

