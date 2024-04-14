from core.rabbitmq.messages.base_request import BaseMessage

GET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE = 'get_toodist_categories_request'


class GetTodoitsCategoriesRequest(BaseMessage):

    def __init__(self):
        super().__init__(GET_TODOIST_CATEGORIES_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
