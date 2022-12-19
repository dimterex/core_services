from modules.core.rabbitmq.messages.base_request import BaseMessage
from modules.core.rabbitmq.messages.configuration.category_model import CategoryModel

SET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE = 'set_todoist_categories_request'
SET_TODOIST_CATEGORIES_REQUEST_CATEGORIES_PROPERTY = 'categories'


class SetTodoistCategoriesRequest(BaseMessage):
    def __init__(self, categories: list[CategoryModel]):
        super().__init__(SET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)
        self.categories = categories

    def serialize(self):
        categories = []
        for category in self.categories:
            categories.append(category.serialize())

        return self.to_json({
            SET_TODOIST_CATEGORIES_REQUEST_CATEGORIES_PROPERTY: categories,
        })

    @staticmethod
    def deserialize(payload):
        raw_categories = payload[SET_TODOIST_CATEGORIES_REQUEST_CATEGORIES_PROPERTY]
        categories: list[CategoryModel] = []
        for category in raw_categories:
            categories.append(CategoryModel.deserialize(category))

        return SetTodoistCategoriesRequest(categories)
