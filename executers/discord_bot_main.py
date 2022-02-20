import os
import sys

from modules.discord_bot.actions.create_task_action import Create_Task_Action
from modules.discord_bot.actions.get_next_meeting_action import Get_Next_Meeting_Action
from modules.discord_bot.actions.help_action import Help_Action
from modules.discord_bot.actions.write_worklog_action import Write_Worklog_Action
from modules.discord_bot.discord_bot import Discord_Bot
from modules.discord_bot.command_controller import Command_Controller
from modules.rabbitmq.messages.api_controller import Api_Controller
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE, DISCORD_SEND_MESSAGE
from modules.rabbitmq.publisher import Publisher
from modules.rabbitmq.receive import Consumer

HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'
DISCORD_TOKEN = 'DISCORD_TOKEN'


def main():
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    discord_token = os.environ[DISCORD_TOKEN]
    port = int(raw_port)

    api_controller = Api_Controller()
    publisher = Publisher(host, port)
    consumer = Consumer(host, port, DISCORD_QUEUE, api_controller)

    command_controller = Command_Controller()
    command_controller.configure(Help_Action(command_controller, publisher))
    command_controller.configure(Write_Worklog_Action(publisher))
    command_controller.configure(Create_Task_Action(publisher))
    command_controller.configure(Get_Next_Meeting_Action(publisher))

    discord_Bot = Discord_Bot(command_controller)

    def send_text(obj):
        promise_id = obj['promise_id']
        message = obj['message']
        discord_Bot.send_message(promise_id, message)

    api_controller.configure(DISCORD_QUEUE, DISCORD_SEND_MESSAGE, send_text)

    consumer.start()
    discord_Bot.run(discord_token)


if __name__ == '__main__':
    print('Starting')
    main()
    print('Started')
