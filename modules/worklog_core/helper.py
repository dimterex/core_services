import datetime

SECONDS_IN_HOUR = 3600
NEEDS_HOURS = 8


def supported_day(date: datetime.datetime):
    if date.weekday() > 4:  # 4 is Friday
        return False
    return True
