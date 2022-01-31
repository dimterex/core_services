import datetime

from modules.common import *

from jira import JIRA

class Jira_Connection:
    def __init__(self, url, login, password):

        jira_options = {
           'server': url,
           'verify': False,
        }
        self.login = login
        self.jira = JIRA(basic_auth=(login, password), options=jira_options)


    def write_meeting(self, issue_id, meetings):
        for meeting in meetings:
            self.jira.add_worklog(issue_id, timeSpent=meeting.duration, started=meeting.date, comment=meeting.name)
            print('{} | {} | {}'.format(meeting.date, meeting.duration, meeting.name))

    def create_subtask(self, name, parrent_issue_id):
        issue = self.jira.issue(parrent_issue_id)

        try:
            result = self.jira.create_issue(project={'key': issue.fields.project.key},
                summary=name,
                issuetype={'name': 'Task'},
                components=[{'name': 'TRD'}],
                assignee={"name": self.login},
                parent={'key': parrent_issue_id})
        except:

            result = self.jira.create_issue(project={'key': issue.fields.project.key},
                summary=name,
                issuetype={'name': 'Task'},
                components=[{'name': 'TRD Team'}],
                assignee={"name": self.login},
                parent={'key': parrent_issue_id})

        return result