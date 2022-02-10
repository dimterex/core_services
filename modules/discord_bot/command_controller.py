class Command_Controller:
    def __init__(self):
        self.commands = []

    def configure(self, action):
        self.commands.append(action)

    def receive_message(self, promise_id: int, message: str):
        for command in self.commands:
            if message.startswith(command.command):
                command.execute(promise_id, message)
