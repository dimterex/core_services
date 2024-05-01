from datetime import timezone, datetime, timedelta


class EpgProgram:
    def __init__(self, start_time: str, stop_time: str, channel_id: str, title: str, description: str, tz: int):
        self.tz = tz
        self.start_time = self.convert_to_utc(start_time)
        self.stop_time = self.convert_to_utc(stop_time)
        self.channel_id = channel_id
        self.title = title
        self.description = description

    def toRaw(self) -> str:
        start = self.start_time.strftime("%Y%m%d%H%M%S %z")
        stop = self.stop_time.strftime("%Y%m%d%H%M%S %z")

        result = f'<programme start="{start}" stop="{stop}" channel="{self.channel_id}">\n'
        result += f'\t<title lang="ru">{self.title}</title>\n'
        if self.description is not None:
            result += f'\t<desc lang="ru">{self.description}</desc>\n'
        result += '</programme>'
        return result

    def convert_to_utc(self, timestamp_str: str):
        # Разбиваем строку на компоненты
        timestamp, offset = timestamp_str.split()
        year = int(timestamp[:4])
        month = int(timestamp[4:6])
        day = int(timestamp[6:8])
        hour = int(timestamp[8:10])
        minute = int(timestamp[10:12])
        second = int(timestamp[12:14])
        utc_offset_hours = int(offset[:3])
        utc_offset_minutes = int(offset[3:])

        # utc_offset = timedelta(hours=utc_offset_hours, minutes=utc_offset_minutes)
        # dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone(utc_offset))
        return datetime(year, month, day, hour, minute, second, tzinfo=timezone(timedelta(hours=self.tz)))
