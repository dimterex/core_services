import datetime

from core.helpers.helper import convert_rawdate_with_timezone_to_datetime
from core.rabbitmq.messages.configuration.category_model import CategoryModel
from core.rabbitmq.messages.configuration.meeting_categories.get_meeting_categories_request import \
    GetMeetingCategoriesRequest
from core.rabbitmq.messages.configuration.todoits_categories.get_todoits_categories_request import \
    GetTodoitsCategoriesRequest
from core.rabbitmq.messages.configuration.urls.get_url_request import GetUrlRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE, JIRA_URL_TYPE, OUTLOOK_QUEUE, \
    JIRA_QUEUE, TODOIST_QUEUE
from core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse
from core.rabbitmq.messages.todoist.get_completed_tasks_request import GetCompletedTasksRequest
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher

from core.rabbitmq.messages.jira_tracker.create_subtask_request import CreateSubTaskRequest
from core.rabbitmq.messages.jira_tracker.write_worklog_request import WriteWorklogsRequest
from core.rabbitmq.messages.todoist.update_label_request import UpdateLabelRequest
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.outlook.outlook_meeting import GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY, GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY, \
    GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY
from worklog_kpi.models.worklog_sqlite_model import WorklogSqliteModel

from worklog_kpi.services.worklog_service import Worklog_Service
from worklog_kpi.services.worklog_storage_service import WorklogStorageService
from worklog_kpi.worklog_periodical import Worklog_By_Periodical


NEEDS_HOURS = 8


class Write_WorkLok_Action:
    def __init__(self,
                 rpc_publisher: RpcPublisher,
                 logger_service: Logger_Service,
                 storage: WorklogStorageService):
        self.storage = storage
        self.logger_service = logger_service
        self.jira_create_task = {}
        self.rpc_publisher = rpc_publisher
        self.TAG = self.__class__.__name__
        get_url_response = self.rpc_publisher.call(CONFIGURATION_QUEUE, GetUrlRequest(JIRA_URL_TYPE))

        if get_url_response.status == ERROR_STATUS_CODE:
            raise Exception(get_url_response.message)
        self.jira_url: str = str(get_url_response.message)

    def write(self, start_time: datetime.datetime) -> StatusResponse:
        self.logger_service.debug(self.TAG, 'Send result message')
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        workLogService = Worklog_Service(start_time)
        self.write_sync(start_time, workLogService)
        self.get_calendar_tasks(start_time, workLogService)
        todoist_error = self.get_competed_tasks(start_time, workLogService)

        if todoist_error is not None:
            return StatusResponse(f'Todoist error: {todoist_error}', ERROR_STATUS_CODE)

        worklogs = []
        for worklog in workLogService.worklogs:
            worklogs.append(worklog.serialize())
        request_write_jira = WriteWorklogsRequest(worklogs)
        response_write_jira = self.rpc_publisher.call(JIRA_QUEUE, request_write_jira)

        if response_write_jira.status == ERROR_STATUS_CODE:
            return response_write_jira

        self.logger_service.debug(self.TAG, 'Ended')
        message = self.get_response_message(workLogService)
        self.storage.add(WorklogSqliteModel(str(start_time.date()), message))
        return StatusResponse(message)

    def get_response_message(self, worklogs_service: Worklog_Service):
        self.logger_service.debug(self.TAG, 'Prepare tasks ...')
        message: list[str] = []
        timelog = worklogs_service.get_summary()
        message.append(f'Day: {worklogs_service.start_time}')
        for worklog in worklogs_service.worklogs:
            url = f'{self.jira_url}/browse/{worklog.issue_id}'
            message.append(f'\t {worklog.duration} | {url} | {worklog.name}')

        message.append(f'\t Summary: {timelog}')
        return '\n'.join(message)

    def get_competed_tasks(self, start_time: datetime.datetime, worklogs_service: Worklog_Service) -> str:
        request = GetCompletedTasksRequest(start_time)
        response = self.rpc_publisher.call(TODOIST_QUEUE, request)

        if response.status == ERROR_STATUS_CODE:
            return response.message

        issues = response.message
        wrote_time = worklogs_service.get_summary()
        tasks_time = NEEDS_HOURS - wrote_time

        if len(issues) > 0:
            tasks_time = tasks_time / len(issues)

        for issue in issues:
            self.check_issues(issue)
            name = issue['name']
            tracker_id = issue['tracker_id']
            worklogs_service.add_worklog(name, worklogs_service.start_time, tracker_id, tasks_time)
        worklogs_service.from_todoist = True
        return None

    def get_calendar_tasks(self, start_time: datetime.datetime, worklogs_service: Worklog_Service):
        self.logger_service.debug(self.TAG, 'Starting modify')

        events_request = GetEventsByDateRequest(start_time)
        events_response = self.rpc_publisher.call(OUTLOOK_QUEUE, events_request)

        categories_request = GetMeetingCategoriesRequest()
        categories_response = self.rpc_publisher.call(CONFIGURATION_QUEUE, categories_request)

        categories: list[CategoryModel] = []
        for category in categories_response.message:
            categories.append(CategoryModel.deserialize(category))

        def find_in_categories_by_name(name: str) -> CategoryModel:
            for category in categories:
                if category.name == name:
                    return category
            return None

        for calendar_item in events_response.message:
            try:
                item_categories = calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_CATEGORIES_PROPERTY]
                if item_categories is None:
                    category = find_in_categories_by_name('')
                else:
                    category = find_in_categories_by_name(item_categories[0])
                    if category is None:
                        category = find_in_categories_by_name('')

                if category.tracker_id is None or category.tracker_id == '':
                    continue

                worklogs_service.add_worklog(calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_NAME_PROPERTY],
                                             convert_rawdate_with_timezone_to_datetime(calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_START_TIME_PROPERTY]),
                                             category.tracker_id,
                                             float(calendar_item[GET_CALENDAR_BY_DATE_RESPONSE_EVENT_DURATION_PROPERTY]))
            except Exception as e:
                self.logger_service.error(self.TAG, f'Error \n\t{e}')

        worklogs_service.from_calendar = True
        self.logger_service.debug(self.TAG, 'Ending modify')

    def check_issues(self, issue):
        name = issue['name']
        issue_category = issue['category']
        tracker_id = issue['tracker_id']
        issue_id = issue['id']

        if tracker_id is not None:
            return

        categories_request = GetTodoitsCategoriesRequest()
        categories_response = self.rpc_publisher.call(CONFIGURATION_QUEUE, categories_request)

        categories: list[CategoryModel] = []
        for category in categories_response.message:
            categories.append(CategoryModel.deserialize(category))

        def find_in_categories_by_name(name: str) -> CategoryModel:
            for category in categories:
                if category.name == name:
                    return category
            return None

        if issue_category is None:
            category = find_in_categories_by_name('')
        else:
            category = find_in_categories_by_name(issue_category)
            if category is None:
                category = find_in_categories_by_name('')

        parent_issue_id = category.tracker_id
        create_task_request = CreateSubTaskRequest(name, parent_issue_id)
        create_task_response = self.rpc_publisher.call(JIRA_QUEUE, create_task_request)
        if create_task_response.status == ERROR_STATUS_CODE:
            raise Exception(create_task_response.message)

        tracker_id = create_task_response.message
        issue['tracker_id'] = tracker_id
        update_label_request = UpdateLabelRequest(issue_id, tracker_id)
        update_label_response = self.rpc_publisher.call(TODOIST_QUEUE, update_label_request)
        self.logger_service.debug(self.TAG, str(update_label_response.serialize()))

    def write_sync(self, start_time: datetime.datetime, worklogs_service: Worklog_Service):
        Worklog_By_Periodical(start_time, self.rpc_publisher, worklogs_service, self.logger_service).modify()
