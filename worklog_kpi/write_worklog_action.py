import datetime
import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, OUTLOOK_QUEUE, JIRA_QUEUE, TODOIST_QUEUE
from modules.core.rabbitmq.messages.jira_tracker.create_subtask_response import CREATE_SUBTASK_RESPONSE_TASK_ID_PROPERTY
from modules.core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from modules.core.rabbitmq.messages.outlook.get_events_by_date_response import \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENTS_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY
from modules.core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, STATUS_RESPONSE_STATUS_PROPERTY, \
    STATUS_RESPONSE_MESSAGE_PROPERTY, StatusResponse
from modules.core.rabbitmq.messages.todoist.get_completed_tasks_request import GetCompletedTasksRequest
from modules.core.rabbitmq.messages.todoist.get_completed_tasks_response import \
    GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from modules.core.rabbitmq.messages.jira_tracker.create_subtask_request import CreateSubTaskRequest
from modules.core.rabbitmq.messages.jira_tracker.write_worklog_request import WriteWorklogsRequest
from modules.core.rabbitmq.messages.todoist.update_label_request import UpdateLabelRequest
from modules.models.configuration import Configuration
from modules.core.log_service.log_service import Logger_Service, DEBUG_LOG_LEVEL, ERROR_LOG_LEVEL
from modules.core.rabbitmq.publisher import Publisher

from worklog_kpi.services.worklog_service import Worklog_Service
from worklog_kpi.worklog_periodical import Worklog_By_Periodical


NEEDS_HOURS = 8


class Write_WorkLok_Action:
    def __init__(self,
                 configuration: Configuration,
                 publisher: Publisher,
                 logger_service: Logger_Service):
        self.logger_service = logger_service
        self.publisher = publisher
        self.configuration = configuration
        self.jira_create_task = {}
        self.rps = RpcPublisher(self.publisher._url)
        self.TAG = self.__class__.__name__

    def write(self, start_time: datetime.datetime) -> StatusResponse:
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Send result message')
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        workLogService = Worklog_Service(start_time)
        self.write_sync(start_time, workLogService)
        self.get_calendar_tasks(start_time, workLogService)
        self.get_competed_tasks(start_time, workLogService)
        request_write_jira = WriteWorklogsRequest(workLogService.worklogs).to_json()
        response_write_jira = self.rps.call(JIRA_QUEUE, request_write_jira)

        if response_write_jira[MESSAGE_PAYLOAD][STATUS_RESPONSE_STATUS_PROPERTY] == ERROR_STATUS_CODE:
            return StatusResponse(ERROR_STATUS_CODE, response_write_jira[MESSAGE_PAYLOAD][STATUS_RESPONSE_MESSAGE_PROPERTY])

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Ended')
        return StatusResponse(message=self.get_response_message(workLogService))

    def get_response_message(self, worklogs_service: Worklog_Service):
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Prepare tasks ...')
        message: list[str] = []
        timelog = worklogs_service.get_summary()
        message.append(f'Day: {worklogs_service.start_time}')
        for worklog in worklogs_service.worklogs:
            url = f'{self.configuration.jira}/browse/{worklog.issue_id}'
            message.append(f'\t {worklog.duration} | {url} | {worklog.name}')

        message.append(f'\t Summary: {timelog}')
        return '\n'.join(message)

    def get_competed_tasks(self, start_time: datetime.datetime, worklogs_service: Worklog_Service):
        request = GetCompletedTasksRequest(start_time).to_json()
        response = self.rps.call(TODOIST_QUEUE, request)
        issues = response[MESSAGE_PAYLOAD][GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY]
        json_object = json.loads(issues)
        wrote_time = worklogs_service.get_summary()
        tasks_time = NEEDS_HOURS - wrote_time

        if len(json_object) > 0:
            tasks_time = tasks_time / len(json_object)

        for issue in json_object:
            name = issue['name']
            category = issue['category']
            tracker_id = issue['tracker_id']
            id = issue['id']
            self.check_issues(name, category, tracker_id, id)
            worklogs_service.add_worklog(name, worklogs_service.start_time, tracker_id, tasks_time)
        worklogs_service.from_todoist = True
        self.apply_data(worklogs_service)

    def get_calendar_tasks(self, start_time: datetime.datetime, worklogs_service: Worklog_Service):
        request = GetEventsByDateRequest(start_time).to_json()
        response = self.rps.call(OUTLOOK_QUEUE, request)

        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Starting modify')

        for calendar_item in response[MESSAGE_PAYLOAD][GET_CALENDAR_BY_DATE_RESPONSE_EVENTS_PROPERTY]:
            try:
                if calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY] is None:
                    category = self.configuration.meetings_categories[None]
                else:

                    if self.configuration.ignore in calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY]:
                        continue

                    if calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY][0] not in self.configuration.meetings_categories:
                        category = self.configuration.meetings_categories[None]
                    else:
                        category = self.configuration.meetings_categories[calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY][0]]

                worklogs_service.add_worklog(calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY],
                                             calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY],
                                             category.jira_issue_id,
                                             calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY])
            except Exception as e:
                self.logger_service.send_log(ERROR_LOG_LEVEL, self.TAG, f'Error \n\t{e}')

        worklogs_service.from_calendar = True
        self.logger_service.send_log(DEBUG_LOG_LEVEL, self.TAG, 'Ending modify')

    def check_issues(self, name: str, issue_category: str, tracker_id: str, issue_id: str):
        if tracker_id is not None:
            return

        if issue_category is None:
            category = self.configuration.tasks_categories[None]
        else:
            if issue_category not in self.configuration.tasks_categories:
                category = self.configuration.tasks_categories[None]
            else:
                category = self.configuration.tasks_categories[issue_category]

        parent_issue_id = category.jira_issue_id
        create_task_request = CreateSubTaskRequest(name, parent_issue_id).to_json()
        create_task_response = self.rps.call(JIRA_QUEUE, create_task_request)

        tracker_id = create_task_response[MESSAGE_PAYLOAD][CREATE_SUBTASK_RESPONSE_TASK_ID_PROPERTY]
        update_label_request = UpdateLabelRequest(tracker_id, issue_id).to_json()
        update_label_response = self.rps.call(TODOIST_QUEUE, update_label_request)

    def apply_data(self, worklogs_service: Worklog_Service):
        if not worklogs_service.from_todoist:
            return
        if not worklogs_service.from_calendar:
            return
        if not worklogs_service.from_config:
            return



    def write_sync(self, start_time: datetime.datetime, worklogs_service: Worklog_Service):
        Worklog_By_Periodical(self.configuration, start_time, worklogs_service, self.logger_service).modify()
        self.apply_data(worklogs_service)


