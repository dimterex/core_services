from datetime import timedelta


from modules.models.TaskCatogory import TasksCategory
from modules.worklog_core.helper import supported_day


class Worklog_By_Periodical:
    def __init__(self, configuration, start_time, end_time, worklogs_service):
        self.worklogs_service = worklogs_service
        self.configuration = configuration
        self.start_time = start_time
        self.end_time = end_time

    def modify(self):
        date_generated = [self.start_time + timedelta(days=x) for x in range(0, (self.end_time-self.start_time).days)]
        hours = 0.5

        for date in date_generated:
            if not supported_day(date):
                continue

            for task in self.configuration.periodical:
                if task not in self.configuration.categories:
                    self.configuration.categories[task] = TasksCategory(task.name, task.jira_issue_id)

                category = self.configuration.categories[task]
                self.worklogs_service.add_worklog(task.name, date, category.jira_issue_id,  hours)
