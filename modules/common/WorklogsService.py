from modules.common import Worklog

class WorklogsService:
    def __init__(self):
        self.worklogs = []
        self.by_dates = {}

    def add_worklog(self, worklog):
        self.worklogs.append(worklog)
        day = worklog.date.date()
        if day not in self.by_dates:
            self.by_dates[day] = []

        self.by_dates[day].append(worklog)

    def get_by_dates(self):
        return self.by_dates