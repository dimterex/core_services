import datetime

from discord_bot.bot.discord_bot import Discord_Bot
from core.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from core.helpers.helper import convert_rawdate_to_datetime, convert_rawdate_with_timezone_to_datetime

from core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher


class Get_Next_Meeting_Action:
    def __init__(self, publisher: RpcPublisher, discordBot: Discord_Bot):
        self.discord_bot = discordBot
        self.publisher = publisher

    def execute(self, promise_id: int, params: []):
        now = datetime.datetime.now()
        start_time = convert_rawdate_to_datetime(f'{now.year}/{now.month}/{now.day}')
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        request = GetEventsByDateRequest(start_time)
        response = self.publisher.call(OUTLOOK_QUEUE, request)
        meetings = response.message
        selected_meetings = []
        start_time = datetime.datetime.now()
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        for meeting in meetings:
            meeting_start = convert_rawdate_with_timezone_to_datetime(meeting['start_time'])
            if start_time > meeting_start:
                continue
            if len(selected_meetings) == 0:
                selected_meetings.append(meeting)
            else:
                first_item = selected_meetings[0]
                if first_item['start_time'] == meeting['start_time']:
                    selected_meetings.append(meeting)

        if len(selected_meetings) == 0:
            self.discord_bot.send_message(promise_id, 'Not meetings today...')
            return

        messages = []
        for meeting in selected_meetings:
            meeting_start = convert_rawdate_with_timezone_to_datetime(meeting['start_time'])
            meeting_start_time = meeting_start.replace(hour=meeting_start.hour + 7)
            message: list[str] = [
                f'Name: {meeting["name"]}'
                f'\n\tDate: {meeting_start_time.day}-{meeting_start_time.month}-{meeting_start_time.year}'
                f'\n\tTime: {meeting_start_time.hour}:{meeting_start_time.minute} ({meeting["duration"]})'
                f'\n\tLocation: {meeting["location"]}'
                f'\n\tContent: {meeting["description"]}'
            ]
            messages.append(''.join(message))
        self.discord_bot.send_message(promise_id, '\n'.join(messages))
