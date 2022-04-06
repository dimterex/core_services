from modules.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.rabbitmq.messages.worklog.write_worklog import Write_Worklog
from modules.rabbitmq.publisher import Publisher


class Write_Worklog_Action:
    def __init__(self, publisher: Publisher):
        self.publisher = publisher

    def execute(self, promise_id: int, messages: []):
        start_date = messages[0]
        self.publisher.send_message(WORKLOG_QUEUE, Write_Worklog(promise_id, start_date).to_json())
