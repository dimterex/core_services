from datetime import datetime

from worklog_kpi.models.worklog import Worklog


class Worklog_Service:
    def __init__(self, start_time: datetime):
        self.start_time = start_time
        self.worklogs: list[Worklog] = []
        self.from_todoist = False
        self.from_calendar = False
        self.from_config = False

    def add_worklog(self, name: str, current_date: datetime, jira_issue: str, need_write_time: float):
        worklog = Worklog(name, current_date, jira_issue, need_write_time)
        self.worklogs.append(worklog)

    def get_summary(self) -> int:
        summary = 0

        for worklog in self.worklogs:
            summary += worklog.duration

        return summary

