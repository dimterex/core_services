import os
import time

from docker_bot.handlers.get_container_with_ports_request_handler import GetContainerWithPortsRequestHandler
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.identificators import DOCKER_QUEUE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    api_controller = RpcApiController(logger_service)
    api_controller.subscribe(GetContainerWithPortsRequestHandler())
    rcp = RpcConsumer(ampq_url, DOCKER_QUEUE, api_controller)
    rcp.start()


if __name__ == '__main__':
    main()
    try:
        while True:
            time.sleep(1)
    finally:
        pass
