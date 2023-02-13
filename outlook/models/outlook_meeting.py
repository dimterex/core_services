import datetime
import json

from exchangelib import CalendarItem

from modules.core.helpers.helper import SECONDS_IN_HOUR

GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY = 'name'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY = 'start_time'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY = 'duration'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY = 'categories'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DESCRIPTION_PROPERTY = 'description'
GET_CALENDAR_BY_DATE_RESPONSE_EVENT_LOCATION_PROPERTY = 'location'


class Outlook_Meeting:
    def __init__(self, raw_outlook_meeting: CalendarItem):
        self.end: datetime.datetime = raw_outlook_meeting.end
        self.start: datetime.datetime = raw_outlook_meeting.start
        self.name: str = raw_outlook_meeting.subject
        self.categories = raw_outlook_meeting.categories
        self.description: str = raw_outlook_meeting.text_body
        self.location = raw_outlook_meeting.location

    def serialize(self):
        difference = self.end - self.start
        dict_object = {
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY: self.name,
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY: str(self.start),
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY: difference.seconds / SECONDS_IN_HOUR,
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY: self.categories,
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DESCRIPTION_PROPERTY: self.description,
            GET_CALENDAR_BY_DATE_RESPONSE_EVENT_LOCATION_PROPERTY: self.location,
        }
        return dict_object
