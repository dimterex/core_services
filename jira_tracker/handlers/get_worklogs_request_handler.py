import calendar
from datetime import datetime, timedelta

from jira_tracker.jira_connection import Jira_Connection
from jira_tracker.models.worklog_day import WorklogDay
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_request import GET_WORKLOGS_REQUEST_YEAR, \
    GET_WORKLOGS_REQUEST_MONTH, GET_WORKLOGS_REQUEST_MESSAGE_TYPE
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetWorklogsRequestHandler(RpcBaseHandler):
    def __init__(self, jira: Jira_Connection, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.jira = jira
        self.TAG = self.__class__.__name__

    def get_message_type(self) -> str:
        return GET_WORKLOGS_REQUEST_MESSAGE_TYPE

    def execute(self, payload) -> StatusResponse:
        year = payload[GET_WORKLOGS_REQUEST_YEAR]
        month = payload[GET_WORKLOGS_REQUEST_MONTH]

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Connecting to jira for get time...')
        userName = self.jira.login.lower()
        num_days = calendar.monthrange(year, month)[1]
        jira = self.jira.connect_to_jira()
        day_statistics: list[dict] = []

        for day in range(1, num_days+1):
            targetDay = datetime(year, month, day)
            nextDay = targetDay + timedelta(days=1)
            issues = jira.search_issues(f'worklogAuthor = "{userName}" AND worklogDate >= "{targetDay.strftime("%Y/%m/%d")}" AND worklogDate < "{nextDay.strftime("%Y/%m/%d")}"')

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

            sum_timespent = 0
            if len(worklogs) != 0:
                for wl in worklogs:
                    sum_timespent += wl.timeSpentSeconds

            day_statistics.append(WorklogDay(targetDay, sum_timespent).to_json())
        jira.close()
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, f'Disconnected to jira for get time... Result: {day_statistics}')
        return StatusResponse(day_statistics)

