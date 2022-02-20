import discord

from modules.discord_bot.command_controller import Command_Controller


class Discord_Bot(discord.Client):
    def __init__(self, command_controller: Command_Controller, **options):
        super().__init__(**options)
        self.command_controller = command_controller
        self.promises = {}
        self.promise_id = 0

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        self.promise_id += 1
        self.promises[self.promise_id] = message.channel.id
        self.command_controller.receive_message(self.promise_id, message.content)
        print(f'Received message: {message}')

    def send_message(self, promise_id, message):
        if promise_id in self.promises:
            channel_id = self.promises[promise_id]
            channel = self.get_channel(channel_id)
            if channel is not None:
                self.loop.create_task(channel.send(message))
        else:
            print(f'Cant send promise: {promise_id}; message: {message}')
