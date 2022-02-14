from exchangelib import CalendarItem


class Outlook_Meeting:
    def __init__(self, raw_outlook_meeting: CalendarItem):
        self.end = raw_outlook_meeting.end
        self.start = raw_outlook_meeting.start
        self.name = raw_outlook_meeting.subject
        self.categories = raw_outlook_meeting.categories
        self.description = raw_outlook_meeting.body
