from core.rabbitmq.messages.base_request import BaseMessage

REMOVE_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE = 'remove_todoist_categories_request.'
REMOVE_TODOIST_CATEGORIES_REQUEST_IDS = 'ids'


class RemoveTodoistCategoriesRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_TODOIST_CATEGORIES_REQUEST_IDS: self.ids
        })

    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_TODOIST_CATEGORIES_REQUEST_IDS]
        return RemoveTodoistCategoriesRequest(ids)
