import os

import requests
from telegram import Update
from tqdm import tqdm
from urllib.parse import urlparse


class FileDownloadCommand:
    def __init__(self, folder: str) -> None:
        self.folder = folder

    async def handle(self, update: Update, url: str):
        if url is None or url == '':
            return

        target_path = os.path.join(self.folder, os.path.basename(urlparse(url).path))
        if os.path.exists(target_path):
            os.remove(target_path)

        message = await update.message.reply_text(f'Downloading {target_path}',
                                                  reply_to_message_id=update.message.message_id)

        response = requests.get(url, verify=False, stream=True)
        if response.status_code == 200:
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=target_path)
            with open(target_path, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
        else:
            await message.edit_text(f'Error code: {response.status_code}')
            return

        await message.edit_text(f'Sending {target_path}')
        with open(target_path, 'rb') as result:
            await update.message.reply_document(result, read_timeout=60 * 5)
            result.close()

        await message.delete()

        if os.path.exists(target_path):
            os.remove(target_path)
