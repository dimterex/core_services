import asyncio
import os

from actions.get_next_meeting_action import Get_Next_Meeting_Action
from actions.write_worklog_action import Write_Worklog_Action
from discord_bot.bot.discord_bot import Discord_Bot
from discord_bot.bot.command_controller import Command_Controller, NEXT_MEETING_COMMAND, WRITE_LOG_COMMAND
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from modules.core.rabbitmq.api_controller import Api_Controller
from modules.core.rabbitmq.messages.identificators import DISCORD_SEND_MESSAGE, DISCORD_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.core.rabbitmq.receive import Consumer

DISCORD_TOKEN = 'DISCORD_TOKEN'
RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


if __name__ == '__main__':
    print('Starting')
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    discord_token = os.environ[DISCORD_TOKEN]

    logger_service = Logger_Service()
    api_controller = Api_Controller(logger_service)
    publisher = Publisher(ampq_url)
    rpc_publisher = RpcPublisher(ampq_url)

    consumer = Consumer(ampq_url, DISCORD_QUEUE, api_controller, logger_service)

    command_controller = Command_Controller()
    discord_Bot = Discord_Bot(command_controller, publisher, logger_service)

    command_controller.configure(WRITE_LOG_COMMAND, Write_Worklog_Action(rpc_publisher, discord_Bot))
    command_controller.configure(NEXT_MEETING_COMMAND, Get_Next_Meeting_Action(rpc_publisher, discord_Bot))

    def send_text(obj):
        promise_id = obj['promise_id']
        message = obj['message']
        discord_Bot.send_message(promise_id, message)
    api_controller.configure(DISCORD_QUEUE, DISCORD_SEND_MESSAGE, send_text)

    consumer.start()

    loop = asyncio.get_event_loop()
    print('Started')
    coro = loop.run_in_executor(None, discord_Bot.bot.run(discord_token))
    loop.run_until_complete(coro)
