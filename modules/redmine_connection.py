import datetime

from redminelib import Redmine
from modules.common import *


class Redmine_Connection:
    def __init__(self, url, login, password):
        self.redmine = Redmine(url, username=login, password=password)


    def write_meeting(self, issue_id, meetings):
        for meeting in meetings:
            time_entry = self.redmine.time_entry.new()
            time_entry.issue_id = issue_id
            time_entry.spent_on = meeting.date
            time_entry.hours = meeting.duration
            time_entry.activity_id = 31
            time_entry.comments = meeting.name
            time_entry.save()
            print('{} | {} | {}'.format(meeting.date, meeting.duration, meeting.name))

