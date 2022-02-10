from modules.discord_bot.command_controller import Command_Controller
from modules.rabbitmq.messages.discord.send_message import Send_Message
from modules.rabbitmq.messages.identificators import DISCORD_QUEUE
from modules.rabbitmq.publisher import Publisher


class Help_Action:
    def __init__(self, command_controller: Command_Controller, publisher: Publisher):
        self.publisher = publisher
        self.command_controller = command_controller
        self.command = '/h'
        self.comment = 'Get supported commands'

    def execute(self, promise_id, message):
        result = []
        result.append('List of command:')
        for command in self.command_controller.commands:
            str = f'\t{command.command} - {command.comment}'
            result.append(str)

        self.publisher.send_message(DISCORD_QUEUE, Send_Message(promise_id, '\n'.join(result)).to_json())


