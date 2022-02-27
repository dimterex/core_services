from datetime import datetime


class Task_Entry:
    def __init__(self, id: int, name: str, date: datetime, category: str, jira_issue: object):
        self.id = id
        self.jira_issue = jira_issue
        self.category = category
        self.date = date
        self.name = name