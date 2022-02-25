import json

from modules.models.task_catogory import TasksCategory


class Configuration:
    def __init__(self, raw_data: str):
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
        self.meetings_categories = {}
        for category in obj['meetings_categories']:
            self.meetings_categories[category['name']] = TasksCategory(category['name'], category['jira_id'])

        self.tasks_categories = {}
        for category in obj['tasks_categories']:
            self.tasks_categories[category['name']] = TasksCategory(category['name'], category['jira_id'])

        self.periodical = []
        for task in obj['periodical']:
            self.periodical.append(TasksCategory(task['name'], task['jira_id']))
