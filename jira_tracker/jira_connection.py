from jira import JIRA

from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel


class Jira_Connection:
    def __init__(self, credentials: CredentialModel, url: str):
        self.credentials = credentials
        self.jira_options = {
            'server': url,
            'verify': False,
        }

    def connect_to_jira(self) -> JIRA:
        return JIRA(basic_auth=(self.credentials.login, self.credentials.password), options=self.jira_options)
