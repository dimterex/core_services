from threading import Thread

from discord.ext import commands

from modules.discord_bot.command_controller import Command_Controller, NEXT_MEETING_COMMAND, WRITE_LOG_COMMAND
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
            await self.bot.process_commands(message)

        @self.bot.command(name=NEXT_MEETING_COMMAND, help="Get next meeting", usage="Without any arguments", description="description")
        async def next_meeting(ctx):
            self.promise_id += 1
            self.promises[self.promise_id] = ctx
            self.command_controller.receive_message(NEXT_MEETING_COMMAND, self.promise_id, [])

        @self.bot.command(name=WRITE_LOG_COMMAND, help="Write log by date", usage="2022/12/30", description="description")
        async def write_log(ctx, datetime):
            self.promise_id += 1
            self.promises[self.promise_id] = ctx
            self.command_controller.receive_message(WRITE_LOG_COMMAND, self.promise_id, [datetime])

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
