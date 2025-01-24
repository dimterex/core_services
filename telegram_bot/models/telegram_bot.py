from telegram import  Update
from telegram.ext import Application, CommandHandler, ContextTypes

from telegram_bot.models.commands.file_download_command import FileDownloadCommand
from telegram_bot.models.commands.pip_download_command import PipDownloadCommand
from telegram_bot.models.commands.webpage_download_command import WebpageDownloadCommand


class TelegramBot:
    def __init__(self, token: str,
                 pipDownloadCommand: PipDownloadCommand,
                 webpageDownloadCommand: WebpageDownloadCommand,
                 fileDownloadCommand: FileDownloadCommand):
        self.application = Application.builder().token(token).post_init(self.post_init).build()
        self.pipDownloadCommand = pipDownloadCommand
        self.webpageDownloadCommand = webpageDownloadCommand
        self.fileDownloadCommand = fileDownloadCommand

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Help!")

    async def pip_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.pipDownloadCommand.handle(update, context.args[0])

    async def web_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.webpageDownloadCommand.handle(update, context.args[0])

    async def file_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.fileDownloadCommand.handle(update, context.args[0])

    async def post_init(self, application: Application) -> None:
        application.add_handler(CommandHandler('pip', self.pip_command))
        application.add_handler(CommandHandler('web', self.web_command))
        application.add_handler(CommandHandler('file', self.file_command))

    def start(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
