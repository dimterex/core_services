import datetime

from modules.common import *

from jira import JIRA

class Jira_Connection:
    def __init__(self, url, login, password):

        jira_options = {
           'server': url,
           'verify': False,
        }

        self.jira = JIRA(basic_auth=(login, password), options=jira_options)


    def write_meeting(self, issue_id, meetings):
        for meeting in meetings:
            self.jira.add_worklog(issue_id, timeSpent=meeting.duration, started=meeting.date, comment=meeting.name)
            print('{} | {} | {}'.format(meeting.date, meeting.duration, meeting.name))