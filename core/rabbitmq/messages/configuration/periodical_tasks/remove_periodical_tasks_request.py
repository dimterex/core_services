from core.rabbitmq.messages.base_request import BaseMessage

REMOVE_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE = 'remove_periodical_tasks_request'
REMOVE_PERIODICAL_TASKS_REQUEST_IDS = 'ids'


class RemovePeriodicalTasksRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_PERIODICAL_TASKS_REQUEST_IDS: self.ids
        })
    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_PERIODICAL_TASKS_REQUEST_IDS]
        return RemovePeriodicalTasksRequest(ids)
