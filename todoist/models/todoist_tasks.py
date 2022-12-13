class Todoist_Tasks:
    def __init__(self, obj: object):
        self.items = []
        for item in obj['items']:
            self.items.append(item['task_id'])
