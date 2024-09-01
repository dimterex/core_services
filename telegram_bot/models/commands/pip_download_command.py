import os
import shutil

from subprocess import Popen, PIPE, STDOUT

from telegram import Update


class PipDownloadCommand:
    
    def __init__(self, folder: str) -> None:
        self.folder = folder

    async def handle(self, update: Update, package_id: str):
        if package_id is None or package_id == '':
            return

        target_path = os.path.join(self.folder, package_id)
        zip_target_path = target_path + '.zip'
        if os.path.exists(target_path):
            shutil.rmtree(target_path)

        if os.path.exists(zip_target_path):
            os.remove(zip_target_path)

        message = await update.message.reply_text(f'Downloading {package_id}', reply_to_message_id=update.message.message_id)

        process = Popen(
            ['pip', 'install', '--target', target_path, package_id],
            stdout=PIPE,
            stderr=PIPE
        )

        with process.stdout:
            self.log_subprocess_output(process.stdout)
        process.wait()  # 0 means success

        await message.edit_text(f'Packaging {package_id}')
        shutil.make_archive(target_path, 'zip', target_path)

        await message.edit_text(f'Sending {package_id}')
        with open(zip_target_path, 'rb') as result:
            await update.message.reply_document(result, read_timeout=60*5)
            result.close()

        await message.delete()

        if os.path.exists(target_path):
            shutil.rmtree(target_path)

        if os.path.exists(zip_target_path):
            os.remove(zip_target_path)

    def log_subprocess_output(self, pipe):
        for line in iter(pipe.readline, b''):  # b'\n'-separated lines
            print(line)
