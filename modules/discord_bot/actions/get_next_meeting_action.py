from modules.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from modules.rabbitmq.messages.outlook.get_next_meeting import Get_Next_Meeting
from modules.rabbitmq.publisher import Publisher


class Get_Next_Meeting_Action:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher
        self.command = '/next_meeting'
        comment = [
            'Get next meeting'
        ]

        self.comment = '\n'.join(comment)

    def execute(self, promise_id, message):
        self.publisher.send_message(OUTLOOK_QUEUE, Get_Next_Meeting(promise_id).to_json())
