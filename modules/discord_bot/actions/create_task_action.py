from modules.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from modules.rabbitmq.messages.outlook.create_task import Create_Task
from modules.rabbitmq.publisher import Publisher


class Create_Task_Action:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher
        self.command = '/create_task'
        comment = [
            'Create task with parameters:'
            '\t--name= test name'
            '\t--start= Datetime (2022/01/01)'
            '\t--duration= 8.0'
            '\t--issue= TASK-1'
        ]

        self.comment = '\n'.join(comment)

    def execute(self, promise_id, message):
        messages = message.split('--')
        start_date = ''
        name = ''
        duration = 0
        issue_id = ''
        for item in messages:
            if 'start' in item:
                start_date = item.replace('start=', '')
            if 'name' in item:
                name = item.replace('name=', '')
            if 'end' in item:
                raw_duration = item.replace('duration=', '')
                duration = float(raw_duration)
            if 'issue' in item:
                issue_id = item.replace('issue=', '')

        self.publisher.send_message(OUTLOOK_QUEUE, Create_Task(promise_id, name, start_date, duration, issue_id).to_json())
