from modules.models.Worklog import Worklog


class Worklog_Service:
    def __init__(self):
        self.worklogs = []
        self.by_dates = {}

    def add_worklog(self, name, current_date, jira_issue, need_write_time):

        worklog = Worklog(name, current_date, jira_issue, need_write_time)

        self.worklogs.append(worklog)
        day = worklog.date.date()
        if day not in self.by_dates:
            self.by_dates[day] = []

        self.by_dates[day].append(worklog)

    def get_by_dates(self):
        return self.by_dates

    def get_summary_by_datetime(self, date):
        day = date.date()
        return self.get_summary_by_date(day)

    def get_summary_by_date(self, date):
        summary = 0

        if date not in self.by_dates:
            return summary

        for worklog in self.by_dates[date]:
            summary += worklog.duration

        return summary

