from exchangelib import Task

ALL_TIME_TO_TASK = 'all='
WROTE_TIME_TO_TASK = 'write='
JIRA_ISSUE_ID = 'jira_issue_id='


class Outlook_Task:
    def __init__(self, raw_outlook_task: Task):
        all_time = None
        write_time = 0
        raw_jira_issue_id = None

        subtest = raw_outlook_task.subject.split(';')
        name = subtest[0]

        for item in subtest:
            if ALL_TIME_TO_TASK in item:
                raw_all_time = item.replace(ALL_TIME_TO_TASK, '')
                if not raw_all_time.isspace():
                    all_time = float(raw_all_time)
            if WROTE_TIME_TO_TASK in item:
                raw_write_time = item.replace(WROTE_TIME_TO_TASK, '')
                if not raw_write_time.isspace():
                    write_time = float(raw_write_time)
            if JIRA_ISSUE_ID in item:
                raw_jira_issue_id = item.replace(JIRA_ISSUE_ID, '')

        self.jira_issue = raw_jira_issue_id
        self.wrote_time = write_time
        self.limit_time = all_time
        self.name = name
        self.raw_outlook_task = raw_outlook_task
        self.start_date = raw_outlook_task.start_date

    def close(self):
        self.raw_outlook_task.complete()
        self.raw_outlook_task.save()
        print(f'All time was wrote: {self.name}')
        pass

    def update_name(self, need_write_time: float):
        self.wrote_time += need_write_time
        self.update_subject()

    def get_categories(self):
        return self.raw_outlook_task.categories

    def update_issue_id(self, new_jira_id):
        self.jira_issue = new_jira_id
        self.update_subject()

    def update_subject(self):
        new_name = []
        new_name.append(self.name)
        if self.limit_time is not None:
            new_name.append(f'{ALL_TIME_TO_TASK}{self.limit_time}')
        new_name.append(f'{WROTE_TIME_TO_TASK}{self.wrote_time}')
        new_name.append(f'{JIRA_ISSUE_ID}{self.jira_issue}')

        self.raw_outlook_task.subject = ';'.join(new_name)
        self.raw_outlook_task.save()
