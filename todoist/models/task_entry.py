from datetime import datetime


class Task_Entry:
    def __init__(self, id: int, name: str, date: datetime, category: str, jira_issue: str):
        self.id = id
        self.jira_issue = jira_issue
        self.category = category
        self.date = date
        self.name = name

    def to_json(self):
        return {
            "name": self.name,
            "category": self.category,
            "tracker_id": self.jira_issue,
            "id": self.id,
        }
