from jira_tracker.jira_connection import Jira_Connection
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from modules.core.rabbitmq.messages.jira_tracker.create_subtask_request import CREATE_SUBTASK_REQUEST_NAME, \
    CREATE_SUBTASK_REQUEST_ROOT_ID, CREATE_SUBTASK_REQUEST_MESSAGE_TYPE
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class CreateSubtaskRequestHandler(RpcBaseHandler):
    def __init__(self, credentials: CredentialModel, jira: Jira_Connection, logger_service: Logger_Service):
        super().__init__(CREATE_SUBTASK_REQUEST_MESSAGE_TYPE)
        self.credentials = credentials
        self.logger_service = logger_service
        self.jira = jira

    def execute(self, payload) -> StatusResponse:
        name = payload[CREATE_SUBTASK_REQUEST_NAME]
        root_id = payload[CREATE_SUBTASK_REQUEST_ROOT_ID]

        self.logger_service.debug(self.TAG, 'Connecting to jira for create subtask...')
        jira = self.jira.connect_to_jira()
        self.logger_service.debug(self.TAG, 'Connected to jira for create subtask...')
        issue = jira.issue(root_id)
        try:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD'}],
                                       assignee={"name": self.credentials.login},
                                       parent={'key': root_id})
        except:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD Team'}],
                                       assignee={"name": self.credentials.login},
                                       parent={'key': root_id})

        jira.close()
        self.logger_service.debug(self.TAG, 'Disconnected to jira for create subtask...')
        return StatusResponse(result.key)
