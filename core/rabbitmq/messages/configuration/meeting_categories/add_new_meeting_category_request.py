from core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_MEETING_CATEGORY_REQUEST_MESSAGE_TYPE = 'add_new_meeting_category_request'


class AddNewMeetingCategoryRequest(BaseMessage):

    def __init__(self):
        super().__init__(ADD_NEW_MEETING_CATEGORY_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
