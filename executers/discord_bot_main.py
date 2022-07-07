import asyncio
import os

from modules.discord_bot.actions.get_next_meeting_action import Get_Next_Meeting_Action
from modules.discord_bot.actions.write_worklog_action import Write_Worklog_Action
from modules.discord_bot.discord_bot import Discord_Bot
from modules.discord_bot.command_controller import Command_Controller, NEXT_MEETING_COMMAND, WRITE_LOG_COMMAND
from modules.models.log_service import Logger_Service
from modules.rabbitmq.messages.api_controller import Api_Controller
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE, DISCORD_SEND_MESSAGE, LOGGER_QUEUE
from modules.rabbitmq.publisher import Publisher
from modules.rabbitmq.receive import Consumer

HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'
DISCORD_TOKEN = 'DISCORD_TOKEN'

if __name__ == '__main__':
    print('Starting')
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    discord_token = os.environ[DISCORD_TOKEN]
    port = int(raw_port)

    logger_service = Logger_Service('Discord_Bot_Application')
    api_controller = Api_Controller(logger_service)
    ampq_url = f'amqp://guest:guest@{host}:{port}'
    publisher = Publisher(ampq_url)

    def send_log(log_message):
        publisher.send_message(LOGGER_QUEUE, log_message.to_json())

    logger_service.configure_action(send_log)

    consumer = Consumer(ampq_url, DISCORD_QUEUE, api_controller, logger_service)

    command_controller = Command_Controller()
    command_controller.configure(WRITE_LOG_COMMAND, Write_Worklog_Action(publisher))
    command_controller.configure(NEXT_MEETING_COMMAND, Get_Next_Meeting_Action(publisher))

    discord_Bot = Discord_Bot(command_controller, publisher, logger_service)

    def send_text(obj):
        promise_id = obj['promise_id']
        message = obj['message']
        discord_Bot.send_message(promise_id, message)
    api_controller.configure(DISCORD_QUEUE, DISCORD_SEND_MESSAGE, send_text)

    consumer.start()

    loop = asyncio.get_event_loop()
    coro = loop.run_in_executor(None, discord_Bot.bot.run(discord_token))
    loop.run_until_complete(coro)
