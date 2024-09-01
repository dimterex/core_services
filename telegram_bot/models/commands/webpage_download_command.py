import os

import docker
from telegram import Update

DOCKER_REMOTE_BASE_URL = 'tcp://server:2375'

class WebpageDownloadCommand:
    def __init__(self, folder: str) -> None:
        self.folder = folder

    async def handle(self, update: Update, url: str):
        if url is None or url == '':
            return

        target_path = os.path.join(self.folder, 'web_path.html')

        if os.path.exists(target_path):
            os.remove(target_path)

        message = await update.message.reply_text(f'Downloading {url}', reply_to_message_id=update.message.message_id)

        client = docker.DockerClient(base_url=DOCKER_REMOTE_BASE_URL)
        container = client.containers.run("capsulecode/singlefilez", f'"{url}"', auto_remove=True)

        with open(target_path, 'wb') as file:
            file.write(container)

        await message.edit_text(f'Packaging {url}')

        await message.edit_text(f'Sending {url}')
        with open(target_path, 'rb') as result:
            await update.message.reply_document(result, read_timeout=60 * 5, reply_to_message_id=update.message.message_id)
            result.close()

        await message.delete()
        if os.path.exists(target_path):
            os.remove(target_path)
