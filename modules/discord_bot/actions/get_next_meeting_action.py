from modules.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from modules.rabbitmq.messages.outlook.create_task import Create_Task
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
        messages = message.split(' ')
        start_date = ''
        name = ''
        duration = 0
        issue_id = ''


        self.publisher.send_message(OUTLOOK_QUEUE, Create_Task(promise_id, name, start_date, duration, issue_id).to_json())
