import os
import socket

import docker
from telegram import Update

from core.log_service.log_service import Logger_Service


class WebpageDownloadCommand:
    def __init__(self, folder: str, logger_service: Logger_Service) -> None:
        self.folder = folder
        self.logger_service = logger_service
        self.TAG = self.__class__.__name__
        host = socket.gethostbyname('server')
        self.DOCKER_REMOTE_BASE_URL = f'tcp://{host}:2375'
        self.logger_service.debug(self.TAG, f'DOCKER_REMOTE_BASE_URL: ' + self.DOCKER_REMOTE_BASE_URL)

    async def handle(self, update: Update, url: str):
        if url is None or url == '':
            return

        target_path = os.path.join(self.folder, 'web_path.html')

        if os.path.exists(target_path):
            os.remove(target_path)
        self.logger_service.debug(self.TAG, f'Downloading {url}')
        message = await update.message.reply_text(f'Downloading {url}', reply_to_message_id=update.message.message_id)

        client = docker.DockerClient(base_url=self.DOCKER_REMOTE_BASE_URL)
        container = client.containers.run("singlefilez", f'"{url}"', auto_remove=True)
        self.logger_service.debug(self.TAG, f'Saving {url}')
        if len(container) == 0:
            self.logger_service.debug(self.TAG, f'Can not download {url}')
            await message.edit_text(f'Can not download page.')
            return

        with open(target_path, 'wb') as file:
            file.write(container)
        self.logger_service.debug(self.TAG, f'Packaging {url}')
        await message.edit_text(f'Packaging {url}')

        self.logger_service.debug(self.TAG, f'Sending {url}')
        await message.edit_text(f'Sending {url}')
        with open(target_path, 'rb') as result:
            await update.message.reply_document(result, read_timeout=60 * 5, reply_to_message_id=update.message.message_id)
            result.close()
        self.logger_service.debug(self.TAG, f'Deleting {url}')
        await message.delete()
        if os.path.exists(target_path):
            os.remove(target_path)
        self.logger_service.debug(self.TAG, f'Done {url}')
