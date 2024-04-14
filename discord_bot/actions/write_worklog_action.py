from discord_bot.bot.discord_bot import Discord_Bot
from core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from core.rabbitmq.messages.status_response import STATUS_RESPONSE_MESSAGE_PROPERTY, StatusResponse
from core.rabbitmq.messages.worklog.write_worklog_request import Write_Worklog_Request
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher


class Write_Worklog_Action:
    def __init__(self, publisher: RpcPublisher, discordBot: Discord_Bot):
        self.discordBot = discordBot
        self.publisher = publisher

    def execute(self, promise_id: int, messages: []):
        start_date = messages[0]

        request = Write_Worklog_Request(start_date)
        response: StatusResponse = self.publisher.call(WORKLOG_QUEUE, request)
        message: str = response.message[STATUS_RESPONSE_MESSAGE_PROPERTY]
        self.discordBot.send_message(promise_id, message)
