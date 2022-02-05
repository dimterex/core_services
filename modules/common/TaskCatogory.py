
class TasksCategory:
    def __init__(self, name, jira_issue_id):
        self.name = name
        self.jira_issue_id = jira_issue_id
        self.meetings = []

    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    def clear(self):
        self.meetings.clear()
