import json
from datetime import datetime, timedelta

from modules.core.helpers.helper import SECONDS_IN_HOUR


class WorklogDay:
    def __init__(self, date: datetime, duration_seconds: int):
        self.date = date
        self.duration: float = duration_seconds / SECONDS_IN_HOUR

    def to_json(self) -> dict:
        return {
            'date': str(self.date.date()),
            'duration': self.duration,
        }
