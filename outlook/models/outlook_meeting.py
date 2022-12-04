import datetime

from exchangelib import CalendarItem


class Outlook_Meeting:
    def __init__(self, raw_outlook_meeting: CalendarItem):
        self.end: datetime.datetime = raw_outlook_meeting.end
        self.start: datetime.datetime = raw_outlook_meeting.start
        self.name: str = raw_outlook_meeting.subject
        self.categories = raw_outlook_meeting.categories
        self.description: str = raw_outlook_meeting.text_body
        self.location = raw_outlook_meeting.location
