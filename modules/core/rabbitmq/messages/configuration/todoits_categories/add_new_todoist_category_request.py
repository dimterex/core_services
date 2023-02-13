from modules.core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_TODOIST_CATEGORY_REQUEST_MESSAGE_TYPE = 'add_new_todoist_category_request'


class AddNewTodoistCategoryRequest(BaseMessage):

    def __init__(self):
        super().__init__(ADD_NEW_TODOIST_CATEGORY_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
