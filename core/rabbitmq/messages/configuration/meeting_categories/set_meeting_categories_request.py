from core.rabbitmq.messages.base_request import BaseMessage
from core.rabbitmq.messages.configuration.category_model import CategoryModel

SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE = 'set_meeting_categories_request'
SET_MEETING_CATEGORIES_REQUEST_CATEGORIES_PROPERTY = 'categories'


class SetMeetingCategoriesRequest(BaseMessage):
    def __init__(self, categories: list[CategoryModel]):
        super().__init__(SET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.categories = categories

    def serialize(self):
        categories = []
        for category in self.categories:
            categories.append(category.serialize())

        return self.to_json({
            SET_MEETING_CATEGORIES_REQUEST_CATEGORIES_PROPERTY: categories,
        })

    @staticmethod
    def deserialize(payload):
        raw_categories = payload[SET_MEETING_CATEGORIES_REQUEST_CATEGORIES_PROPERTY]
        categories: list[CategoryModel] = []
        for category in raw_categories:
            categories.append(CategoryModel.deserialize(category))

        return SetMeetingCategoriesRequest(categories)
