import calendar
import threading
from datetime import datetime, timedelta

from jira_tracker.jira_connection import Jira_Connection
from jira_tracker.models.worklog_day import WorklogDay
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel


class History_Service:
    def __init__(self, credentials: CredentialModel, jira: Jira_Connection, logger_service: Logger_Service):
        # [year][month] = [worklogs]
        self.statistics: dict[int, dict[int, list[WorklogDay]]] = {}
        self.credentials = credentials
        self.logger_service = logger_service
        self.jira = jira
        self.TAG = self.__class__.__name__

        today = datetime.now().date()
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        for month in months:
            if month > today.month:
                continue
            self.update_from_jira(today.year, month)

        for month in months:
            self.update_from_jira(today.year - 1, month)

    def get_statistic(self, year: int, month: int) -> list[WorklogDay]:
        if year not in self.statistics:
            return []
        if month in self.statistics[year]:
            return self.statistics[year][month]
        return []

    def update_date(self, date: datetime, duration: int):
        year = date.year
        month = date.month
        if year not in self.statistics:
            return
        days = self.statistics[year][month]
        for day in days:
            if day.date.date() == date.date():
                day.duration += duration

    def update_from_jira(self, year: int, month: int):
        threading.Thread(target=self.update, args=(year, month)).start()

    def update(self, year: int, month: int):
        userName = self.credentials.login.lower()
        num_days = calendar.monthrange(year, month)[1]
        jira = self.jira.connect_to_jira()

        if year not in self.statistics:
            self.statistics[year] = {}

        self.statistics[year][month] = []
        start_time = datetime.now()
        self.logger_service.trace(self.TAG, f'Connecting to jira for get time {year} {month}: {start_time}')

        for day in range(1, num_days+1):
            targetDay = datetime(year, month, day)
            nextDay = targetDay + timedelta(days=1)

            # start_issues_time = datetime.now()
            # self.logger_service.trace(self.TAG, f'Starting time for search_issues: {start_issues_time}')

            issues = jira.search_issues(f'worklogAuthor = "{userName}" AND worklogDate >= "{targetDay.strftime("%Y/%m/%d")}" AND worklogDate < "{nextDay.strftime("%Y/%m/%d")}"')

            # end_issues_time = datetime.now()
            # self.logger_service.trace(self.TAG, f'End time for search_issues: {end_issues_time}. Diff: {end_issues_time - start_issues_time}')

            worklogs = []
            for issue in issues:
                issueWorklogs = jira.worklogs(issue.key)

                filtredIssueWorklogs = list(filter(lambda o: o.author.name.lower() == userName
                                                             and datetime.strptime(o.created, '%Y-%m-%dT%H:%M:%S.%f%z').date() >= targetDay.date()
                                                             and datetime.strptime(o.started, '%Y-%m-%dT%H:%M:%S.%f%z').date() >= targetDay.date()
                                                             and datetime.strptime(o.started, '%Y-%m-%dT%H:%M:%S.%f%z').date() < nextDay.date()
                                                   , issueWorklogs))

                if len(filtredIssueWorklogs) > 0:
                    worklogs.extend(filtredIssueWorklogs)
            # end_worklogs_time = datetime.now()
            #self.logger_service.trace(self.TAG, f'End time for worklogs: {end_worklogs_time}. Diff: {end_worklogs_time - end_issues_time}')

            sum_timespent = 0
            if len(worklogs) != 0:
                for wl in worklogs:
                    sum_timespent += wl.timeSpentSeconds

            self.statistics[year][month].append(WorklogDay(targetDay, sum_timespent))

        end_time = datetime.now()
        self.logger_service.trace(self.TAG, f'Ending time for get time {year} {month}: {end_time} ({end_time - start_time})')
        # self.logger_service.debug(self.TAG, f'Disconnected to jira for get time... Result: {day_statistics}')
        jira.close()
