from jira import JIRA

from modules.core.log_service.log_service import Logger_Service

class Jira_Connection:
    def __init__(self, url: str, login: str, password: str, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.jira_options = {
            'server': url,
            'verify': False,
        }
        self.login = login
        self.password = password

    def connect_to_jira(self) -> JIRA:
        return JIRA(basic_auth=(self.login, self.password), options=self.jira_options)
