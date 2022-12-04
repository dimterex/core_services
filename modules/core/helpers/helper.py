from datetime import datetime

SECONDS_IN_HOUR = 3600


def convert_rawdate_to_datetime(raw_date: str):
    try:
        # convert from string format to datetime format
        return datetime.strptime(raw_date, '%Y/%m/%d')
    except:
        return datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')


def convert_rawdate_with_timezone_to_datetime(raw_date: str):
    return datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S%z')
