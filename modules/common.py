import json


class Meeting:
    def __init__(self, name, date, duration):
        self.name = name
        self.date = date
        self.duration = duration


class Config:
    def __init__(self, raw_data):
        obj = json.loads(raw_data)
        self.login = obj['login']
        self.password = obj['password']
        self.email = obj['email']
        self.domain = obj['domain']

        self.jira = obj['jira_url']
        self.redmine = obj['redmine_url']
        self.outlook = obj['outlook_url']
        self.confluence = obj['confluence_url']

        self.ignore = obj['ignore']
        self.categories = {}
        for category in obj['categories']:
            self.categories[category['name']] = TasksCategory(category['name'], category['jira_id'], category['redmine_id'])

        self.periodical = []
        for task in obj['periodical']:
            self.periodical.append(TasksCategory(task['name'], task['jira_id'], task['redmine_id']))

    def clear_categories(self):
        for cat in self.categories:
            self.categories[cat].clear()
        for cat in self.periodical:
            cat.clear()


class TasksCategory:
    def __init__(self, name, jira_issue_id, redmine_issue_id):
        self.name = name
        self.jira_issue_id = jira_issue_id
        self.redmine_issue_id = redmine_issue_id
        self.meetings = []

    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    def clear(self):
        self.meetings.clear()
