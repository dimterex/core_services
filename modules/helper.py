SECONDS_IN_HOUR = 3600


def supported_day(date):
    if date.weekday() > 4:  # 4 is Friday
        return False
    return True
