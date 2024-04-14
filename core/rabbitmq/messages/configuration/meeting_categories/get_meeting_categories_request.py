from core.rabbitmq.messages.base_request import BaseMessage

GET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE = 'get_meeting_categories_request'


class GetMeetingCategoriesRequest(BaseMessage):

    def __init__(self):
        super().__init__(GET_MEETING_CATEGORIES_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
