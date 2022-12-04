import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

GET_CALENDAR_BY_DATE_RESPONSE = 'get_calendar_by_date_response'
GET_CALENDAR_BY_DATE_RESPONSE_EVENTS_PROPERTY = 'events'


GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY = 'name'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY = 'start_time'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY = 'duration'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY = 'categories'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DESCRIPTION_PROPERTY = 'description'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_LOCATION_PROPERTY = 'location'


class GetEventsByDateResponse:
    def __init__(self, events: list):
        self.events = events

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_CALENDAR_BY_DATE_RESPONSE,
            MESSAGE_PAYLOAD: {
                GET_CALENDAR_BY_DATE_RESPONSE_EVENTS_PROPERTY: self.events,
            }
        }
        return json.dumps(dict_object)

