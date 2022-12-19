from datetime import datetime

from modules.models.configuration import Configuration
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.models.task_catogory import TasksCategory
from worklog_kpi.services.worklog_service import Worklog_Service


class Worklog_By_Periodical:
    def __init__(self,
                 configuration: Configuration,
                 start_time: datetime,
                 worklog_service: Worklog_Service,
                 logger_service: Logger_Service):
        self.logger_service = logger_service
        self.worklog_service = worklog_service
        self.configuration = configuration
        self.start_time = start_time

    def modify(self):
        self.logger_service.debug(self.__class__.__name__, 'Starting modify')
        hours = 0.5

        for task in self.configuration.periodical:
            if task not in self.configuration.meetings_categories:
                self.configuration.meetings_categories[task] = TasksCategory(task.name, task.jira_issue_id)

            category = self.configuration.meetings_categories[task]
            self.worklog_service.add_worklog(task.name, self.start_time.replace(hour=7), category.jira_issue_id, hours)
        self.worklog_service.from_config = True
        self.logger_service.debug(self.__class__.__name__, 'Ending modify')
