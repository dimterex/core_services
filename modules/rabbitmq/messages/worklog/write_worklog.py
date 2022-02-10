import json

from modules.rabbitmq.messages.identificators import WORKLOG_WRITE_MESSAGE


class Write_Worklog:
    def __init__(self, promise_id, start_day, end_date):
        self.end_date = end_date
        self.start_day = start_day
        self.promise_id = promise_id

    def to_json(self):
        dict_object = {
            'type': WORKLOG_WRITE_MESSAGE,
            'value': {
                'promise_id': self.promise_id,
                'start_day': self.start_day,
                'end_date': self.end_date,
            }
        }
        return json.dumps(dict_object)

