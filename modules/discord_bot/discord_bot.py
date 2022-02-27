import asyncio
from threading import Thread

from discord.ext import commands

from modules.discord_bot.command_controller import Command_Controller
from modules.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from modules.rabbitmq.messages.outlook.get_next_meeting import Get_Next_Meeting
from modules.rabbitmq.publisher import Publisher


class Discord_Bot():
    def __init__(self, command_controller: Command_Controller, publisher: Publisher):
        self.publisher = publisher
        self.command_controller = command_controller
        self.promises = {}
        self.promise_id = 0
        self.bot = commands.Bot(command_prefix='/')

        @self.bot.event
        async def on_command_error(ctx, error):
            await ctx.send(error)

        @self.bot.event
        async def on_ready():
            print('We have logged in as {0.user}'.format(self.bot))

        @self.bot.event
        async def on_command_error(ctx, error):
            await ctx.send(error)

        @self.bot.event
        async def on_message(message):
            self.promise_id += 1
            self.promises[self.promise_id] = message.channel
            self.command_controller.receive_message(self.promise_id, message.content)
            print(f'Discord received message: {message.content}')
            await self.bot.process_commands(message)

    def send_message(self, promise_id, message):
        if promise_id in self.promises:
            channel = self.promises[promise_id]
            if channel is not None:
                self.bot.loop.create_task(channel.send(message))
            self.promises.pop(promise_id)
        else:
            print(f'Cant send promise: {promise_id}; message: {message}')

    def initialize(self, token: str):
        print('Discord_Bot started.')

        def run():
            self.bot.start(token)

        th = Thread(target=run, name='discord', daemon=True)
        th.start()

        print('Discord_Bot starting.')
