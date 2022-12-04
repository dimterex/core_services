class Todoist_Tasks:
    def __init__(self, obj: object):
        self.items = []
        for item in obj['items']:
            self.items.append(Task_Item(item))


class Task_Item:
    def __init__(self, obj: object):
        self.content = obj['content']
        self.meta_data = obj['meta_data']
        self.user_id = obj['user_id']
        self.task_id = obj['task_id']
        self.project_id = obj['project_id']
        self.completed_date = obj['completed_date']
        self.id = obj['id']
