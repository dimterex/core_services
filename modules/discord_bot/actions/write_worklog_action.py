from modules.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.rabbitmq.messages.worklog.write_worklog import Write_Worklog
from modules.rabbitmq.publisher import Publisher


class Write_Worklog_Action:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher
        self.command = '/write_time'
        comment = [
            'Write time by period:'
            '\t--start= Datetime (2022/01/01)'
            '\t--end= Datetime (2022/01/12)'
        ]

        self.comment = '\n'.join(comment)

    def execute(self, promise_id, message):
        messages = message.split(' ')
        start_date = ''
        end_date = ''
        for item in messages:
            if '--start' in item:
                start_date = item.replace('--start=', '')
            if '--end' in item:
                end_date = item.replace('--end=', '')

        self.publisher.send_message(WORKLOG_QUEUE, Write_Worklog(promise_id, start_date, end_date).to_json())
