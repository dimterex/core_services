from modules.core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE = 'add_new_periodical_task_request'


class AddNewPeriodicalTaskRequest(BaseMessage):

    def __init__(self):
        super().__init__(ADD_NEW_PERIODICAL_TASK_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
