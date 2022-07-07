import asyncio
import threading

from modules.logger_viewer.messages.LogModel import LogModel
from websocket_server import WebsocketServer

class WebSocketService:
    def __init__(self, host: str, port: int):
        self.server = WebsocketServer(host=host, port=port)

        def run():
            self.server.run_forever()

        th = threading.Thread(target=run, name='websocket', daemon=True)
        th.start()

    def send_log(self, logMessage: LogModel):
        self.server.send_message_to_all(logMessage.to_json())

