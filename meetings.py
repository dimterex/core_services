import sys, getopt

from modules.common.Configuration import Config
from modules.common.WorklogsService import WorklogsService
from modules.jira_connection import Jira_Connection
from modules.meetings_writer import Worklog_by_Meetings
from modules.outlook_connection import Outlook_Connection

from datetime import datetime
from tzlocal import get_localzone

import warnings

from modules.worklog_periodical import Worklog_By_Periodical
from modules.worklog_tasks import Worklog_By_Tasks

SETTINGS_FILE = 'settings.json'


def save_file(meetings):
    with open('black_list', 'a', encoding='utf8') as file:
        file.write('-----------{} at {}\n'.format("Black list", datetime.now().strftime("%y-%m-%d")))

        for meeting in meetings:
            file.write('{}, {}, {}\n'.format(meeting.name, meeting.date, meeting.duration))

        file.write('\n')


def convert_rawdate_to_datetime(raw_date):
    # convert from string format to datetime format
    return datetime.strptime(raw_date, '%Y/%m/%d')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    try:
        arguments, values = getopt.getopt(sys.argv[1:], "hi:o:", ["start_time=", "end_time="])
    except getopt.GetoptError:
        print('meetings.py --start_time <start_time> --end_time <end_time>')
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s", "--start_time"):
            # print ('start_time = {}'.format(currentValue))
            start_time = convert_rawdate_to_datetime(currentValue)

        elif currentArgument in ("-e", "--end_time"):
            # print ('end_time = {}'.format(currentValue))
            end_time = convert_rawdate_to_datetime(currentValue)

    with open(SETTINGS_FILE, 'r', encoding='utf8') as json_file:
        raw_data = json_file.read()
        сonfiguration = Config(raw_data)

    local_tz = get_localzone()
    start_time = start_time.replace(tzinfo=local_tz)
    end_time = end_time.replace(tzinfo=local_tz)

    сonfiguration.clear_categories()
    jira_connection = Jira_Connection(сonfiguration.jira, сonfiguration.login, сonfiguration.password)
    domain_login = f'{сonfiguration.domain}\\{сonfiguration.login}'
    outlook_connection = Outlook_Connection(сonfiguration.outlook, сonfiguration.email, domain_login,
                                            сonfiguration.password)

    worklogs_service = WorklogsService()
    worklog_by_Meetings = Worklog_by_Meetings(сonfiguration, start_time, end_time, jira_connection, outlook_connection, worklogs_service)
    worklog_by_Meetings.modify()

    # сonfiguration.clear_categories()
    worklog_By_Periodical = Worklog_By_Periodical(сonfiguration, start_time, end_time, worklogs_service)
    worklog_By_Periodical.modify()

    # сonfiguration.clear_categories()
    worklog_By_Tasks = Worklog_By_Tasks(сonfiguration, start_time, end_time, jira_connection, outlook_connection, worklogs_service)
    worklog_By_Tasks.modify()

    by_dates = worklogs_service.get_by_dates()
    for dates in by_dates:
        timelog = 0

        print(f'Day: {dates}')
        for worklog in by_dates[dates]:
            timelog += worklog.duration
            print(f'\t {worklog.duration} | {worklog.issue_id} | {worklog.name}')

        print(f'\t Summary: {timelog}')

