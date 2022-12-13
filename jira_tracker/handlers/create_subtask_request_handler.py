from jira_tracker.jira_connection import Jira_Connection
from modules.core.rabbitmq.messages.jira_tracker.create_subtask_request import CREATE_SUBTASK_REQUEST_NAME, \
    CREATE_SUBTASK_REQUEST_ROOT_ID, CREATE_SUBTASK_REQUEST_MESSAGE_TYPE
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL
from modules.core.rabbitmq.messages.status_response import StatusResponse
from modules.core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class CreateSubtaskRequestHandler(RpcBaseHandler):
    def __init__(self, jira: Jira_Connection, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.jira = jira
        self.login = self.jira.login
        self.TAG = self.__class__.__name__

    def get_message_type(self) -> str:
        return CREATE_SUBTASK_REQUEST_MESSAGE_TYPE

    def execute(self, payload) -> StatusResponse:
        name = payload[CREATE_SUBTASK_REQUEST_NAME]
        root_id = payload[CREATE_SUBTASK_REQUEST_ROOT_ID]

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Connecting to jira for create subtask...')
        jira = self.jira.connect_to_jira()
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Connected to jira for create subtask...')
        issue = jira.issue(root_id)
        try:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD'}],
                                       assignee={"name": self.login},
                                       parent={'key': root_id})
        except:
            result = jira.create_issue(project={'key': issue.fields.project.key},
                                       summary=name,
                                       issuetype={'name': 'Task'},
                                       components=[{'name': 'TRD Team'}],
                                       assignee={"name": self.login},
                                       parent={'key': root_id})

        jira.close()
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Disconnected to jira for create subtask...')
        return StatusResponse(result.key)

