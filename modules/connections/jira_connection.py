from jira import JIRA


class Jira_Connection:
    def __init__(self, url, login, password):
        jira_options = {
            'server': url,
            'verify': False,
        }
        self.login = login
        # self.jira = JIRA(basic_auth=(login, password), options=jira_options)

    def write_worklogs(self, worklogs):
        for worklog in worklogs:
            # self.jira.add_worklog(worklog.issue_id, timeSpent=worklog.duration, started=worklog.date, comment=worklog.name)
            pass

    def create_subtask(self, name, parent_issue_id):
        issue = self.jira.issue(parent_issue_id)

        try:
            result = self.jira.create_issue(project={'key': issue.fields.project.key},
                                            summary=name,
                                            issuetype={'name': 'Task'},
                                            components=[{'name': 'TRD'}],
                                            assignee={"name": self.login},
                                            parent={'key': parent_issue_id})
        except:

            result = self.jira.create_issue(project={'key': issue.fields.project.key},
                                            summary=name,
                                            issuetype={'name': 'Task'},
                                            components=[{'name': 'TRD Team'}],
                                            assignee={"name": self.login},
                                            parent={'key': parent_issue_id})

        return result
