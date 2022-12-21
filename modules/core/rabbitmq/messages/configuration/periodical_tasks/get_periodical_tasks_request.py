from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE = 'get_periodical_tasks_request'


class GetPeriodicalTasksRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
