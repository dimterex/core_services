import json

from modules.common.TaskCatogory import TasksCategory

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
            self.categories[category['name']] = TasksCategory(category['name'], category['jira_id'])

        self.periodical = []
        for task in obj['periodical']:
            self.periodical.append(TasksCategory(task['name'], task['jira_id']))

    def clear_categories(self):
        for cat in self.categories:
            self.categories[cat].clear()
        for cat in self.periodical:
            cat.clear()