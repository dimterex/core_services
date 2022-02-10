from datetime import datetime, date

from modules.models.worklog import Worklog


class Worklog_Service:
    def __init__(self):
        self.worklogs: list[Worklog] = []
        self.by_dates: dict[date, list[Worklog]] = {}

    def add_worklog(self, name: str, current_date: datetime, jira_issue: str, need_write_time: float):
        worklog = Worklog(name, current_date, jira_issue, need_write_time)

        self.worklogs.append(worklog)
        day = worklog.date.date()
        if day not in self.by_dates:
            self.by_dates[day] = []

        self.by_dates[day].append(worklog)

    def get_by_dates(self):
        return self.by_dates

    def get_summary_by_datetime(self, datestamp: datetime):
        day = datestamp.date()
        return self.get_summary_by_date(day)

    def get_summary_by_date(self, datestamp: date):
        summary = 0

        if datestamp not in self.by_dates:
            return summary

        for worklog in self.by_dates[datestamp]:
            summary += worklog.duration

        return summary

