from modules.worklog_core.helper import SECONDS_IN_HOUR


class Worklog_by_Meetings:
    def __init__(self, configuration, start_time, end_time, issue_tracker, outlook, worklogs_service):
        self.worklogs_service = worklogs_service
        self.configuration = configuration
        self.start_time = start_time
        self.end_time = end_time
        self.issue_tracker = issue_tracker
        self.outlook = outlook

    def modify(self):
        meetings = self.outlook.get_meeting(self.start_time, self.end_time)

        for calendar_item in meetings:
            difference = calendar_item.end - calendar_item.start

            if calendar_item.categories is None:
                category = self.configuration.categories[None]
            else:

                if self.configuration.ignore in calendar_item.categories:
                    continue

                if calendar_item.categories[0] not in self.configuration.categories:
                    category = self.configuration.categories[None]
                else:
                    category = self.configuration.categories[calendar_item.categories[0]]

            self.worklogs_service.add_worklog(calendar_item.subject, calendar_item.start, category.jira_issue_id,
                                              difference.seconds / SECONDS_IN_HOUR)
