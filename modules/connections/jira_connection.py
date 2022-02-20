from jira import JIRA

from modules.models.worklog import Worklog


class Jira_Connection:
    def __init__(self, url: str, login: str, password: str):
        self.jira_options = {
            'server': url,
            'verify': False,
        }
        self.login = login
        self.password = password

    def write_worklogs(self, worklogs: list[Worklog]):
        print('Connecting to jira for write worklogs...')
        jira = JIRA(basic_auth=(self.login, self.password), options=self.jira_options)
        print('Connected to jira for write worklogs...')
        for worklog in worklogs:
            jira.add_worklog(worklog.issue_id, timeSpent=f'{worklog.duration}', started=worklog.date, comment=worklog.name)
        jira.close()
        print('Disconnected to jira for write worklogs...')

    def create_subtask(self, name: str, parent_issue_id: str):
        print('Connecting to jira for create subtask...')
        jira = JIRA(basic_auth=(self.login, self.password), options=self.jira_options)
        print('Connected to jira for create subtask...')
        issue = jira.issue(parent_issue_id)

        try:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD'}],
                                       assignee={"name": self.login},
                                       parent={'key': parent_issue_id})
        except:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD Team'}],
                                       assignee={"name": self.login},
                                       parent={'key': parent_issue_id})

        jira.close()
        print('Disconnected to jira for create subtask...')
        return result




