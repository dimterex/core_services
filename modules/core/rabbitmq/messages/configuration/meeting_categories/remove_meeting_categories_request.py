from modules.core.rabbitmq.messages.base_request import BaseMessage

REMOVE_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE = 'remove_meeting_categories_request'
REMOVE_MEETING_CATEGORIES_REQUEST_IDS = 'ids'


class RemoveMeetingCategoriesRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_MEETING_CATEGORIES_REQUEST_IDS: self.ids
        })

    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_MEETING_CATEGORIES_REQUEST_IDS]
        return RemoveMeetingCategoriesRequest(ids)
