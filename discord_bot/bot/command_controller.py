NEXT_MEETING_COMMAND = 'next_meeting'
WRITE_LOG_COMMAND = 'write'


class Command_Controller:
    def __init__(self):
        self.commands = {}

    def configure(self, command: str, action):
        self.commands[command] = action

    def receive_message(self, command: str, promise_id: int, argumets: []):
        if command in self.commands:
            self.commands[command].execute(promise_id, argumets)
