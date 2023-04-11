import os
import socket
import time
import warnings

from modules.core.rabbitmq.messages.configuration.tokens.get_token_request import GetTokenRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, TRACKS_QUEUE, YANDEX_TOKEN
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE
from modules.core.rabbitmq.messages.tracks.get_track_metadata_request import GetTrackMetadataRequest
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from modules.core.log_service.log_service import Logger_Service
import ipaddress

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
DOWNLOAD_DIRECTORY_PATH = '/downloads'


def main():
    logger_service = Logger_Service()

    import socket
    urls = [
        "chat.openai.com",
        "auth0.openai.com",
        "openai.com",
        "cdn.auth0.com",
        "cdn.openai.com",
    ]

    # получаем список всех IP-адресов, связанных с URL
    ip_list = []
    ip_subnet_list_1 = []
    ip_subnet_list = []
    for url in urls:
        for addr in socket.getaddrinfo(url, None):
            ip = addr[4][0]
            if ip not in ip_list:
                ip_list.append(ip)
        try:
            # Получение информации об IP-адресах для домена
            _, _, ips = socket.gethostbyname_ex(url)
            for ip in ips:
                # Разбиение IP-адреса на подсеть и маску
                if '/' in ip:
                    ip_addr, subnet_mask = ip.split('/')
                else:
                    ip_addr = ip
                    subnet_mask = None
                # Добавление подсети и маски в список
                ip_subnet_list_1.append((str(url), str(ip_addr), str(subnet_mask)))
        except socket.gaierror:
            print(f"Не удалось получить IP-адреса для домена {url}")

        ip_address = socket.gethostbyname(url)

        for response in socket.getaddrinfo(ip_address, None):
            ip_subnet = response[-1][0]
            if ip_subnet not in ip_subnet_list:
                ip_subnet_list.append(ip_subnet)

    # выводим список IP-адресов
    print(ip_list)
    print('')
    print("URL\t\tIP\t\tMask")
    for row in sorted(ip_subnet_list_1):
        print("\t\t".join(row))
    print('')
    print(ip_subnet_list)

    # Создание пустой таблицы
    table = []

    # Преобразование строковых адресов в объекты ipaddress.IPv4Network
    ip_subnet_list = [ipaddress.IPv4Network(subnet) for subnet in ip_list]

    # Проход по списку подсетей и исключение подмножеств
    for i, subnet1 in enumerate(ip_subnet_list):
        exclude = False
        for j, subnet2 in enumerate(ip_subnet_list):
            # Пропуск подсети, если она является сама себе или если ее нет в списке
            if i == j or not subnet2:
                continue
            # Исключение подмножеств
            if subnet1.subnet_of(subnet2):
                exclude = True
                break
        if not exclude:
            # Добавление подходящей подсети в таблицу
            table.append((str(subnet1.network_address), str(subnet1.prefixlen), str(subnet1.netmask)))

    # Вывод таблицы на экран
    print("IP-адрес\t\tПрефикс\t\tМаска")
    for row in sorted(table):
        print("\t\t".join(row))
    # ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    # rpc_publisher = RpcPublisher(ampq_url)
    #
    # token_response = rpc_publisher.call(CONFIGURATION_QUEUE, GetTokenRequest(YANDEX_TOKEN))
    #
    # if token_response.status == ERROR_STATUS_CODE:
    #     raise Exception(token_response.message)
    # yandexService = YandexMusicService(str(token_response.message), DOWNLOAD_DIRECTORY_PATH, logger_service)
    # trackService = TagsService(logger_service)
    #
    # download_handler = DownloadLikesTracksHandler(yandexService, trackService, logger_service, rpc_publisher)
    # download_handler.start()
    # api_controller = RpcApiController(logger_service)
    # rcp = RpcConsumer(ampq_url, TRACKS_QUEUE, api_controller)
    # api_controller.subscribe(GetTrackMetadataRequestHandler(logger_service, yandexService))
    # rcp.start()
    # comparing_handler = ComparingTrackInfoHandler(DOWNLOAD_DIRECTORY_PATH, yandexService, trackService, logger_service, rpc_publisher)
    # comparing_handler.start('/music')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')

