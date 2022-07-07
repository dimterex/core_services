from datetime import datetime

from modules.connections.jira_connection import Jira_Connection
from modules.connections.outlook_connection import Outlook_Connection
from modules.models.configuration import Configuration
from modules.models.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.worklog_core.services.worklog_service import Worklog_Service


SECONDS_IN_HOUR = 3600


class Worklog_by_Meetings:
    def __init__(self,
                 configuration: Configuration,
                 start_time: datetime,
                 issue_tracker: Jira_Connection,
                 outlook: Outlook_Connection,
                 worklog_service: Worklog_Service,
                 logger_service: Logger_Service):
        self.logger_service = logger_service
        self.worklog_service = worklog_service
        self.configuration = configuration
        self.start_time = start_time
        self.issue_tracker = issue_tracker
        self.outlook = outlook

    def modify(self):
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Starting modify')
        meetings = self.outlook.get_meeting(self.start_time)

        for calendar_item in meetings:
            difference = calendar_item.end - calendar_item.start

            if calendar_item.categories is None:
                category = self.configuration.meetings_categories[None]
            else:

                if self.configuration.ignore in calendar_item.categories:
                    continue

                if calendar_item.categories[0] not in self.configuration.meetings_categories:
                    category = self.configuration.meetings_categories[None]
                else:
                    category = self.configuration.meetings_categories[calendar_item.categories[0]]

            self.worklog_service.add_worklog(calendar_item.name, calendar_item.start, category.jira_issue_id,
                                             difference.seconds / SECONDS_IN_HOUR)
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.__class__.__name__, 'Ending modify')
