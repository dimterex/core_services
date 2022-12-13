import json
import threading

from websocket_server import WebsocketServer

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_PAYLOAD, MESSAGE_TYPE


class WebSocketService:
    def __init__(self, host: str, port: int):
        self.server = WebsocketServer(host=host, port=port)
        self.clients = []
        self.promises = {}
        self.handlers = {}
        self.promise = 0
        self.promises_map = {}

        def new_client(client, server):
            self.clients.append(client)

        def left_client(client, server):
            self.clients.remove(client)

        def message_received(client, server, message):
            self.parse_message(client, message)

        self.server.set_fn_new_client(new_client)
        self.server.set_fn_client_left(left_client)
        self.server.set_fn_message_received(message_received)

        def run():
            self.server.run_forever()

        th = threading.Thread(target=run, name='websocket', daemon=True)
        th.start()

    def map_promise_id(self, external_promise_id) -> int:
        self.promise += 1
        self.promises_map[self.promise] = external_promise_id
        return self.promise

    def get_real_promise(self, internal_promise_id) -> int:
        return self.promises_map[internal_promise_id]

    def configute(self, type: str, callback):
        self.handlers[type] = callback

    def send_message(self, external_promise_id: int, message: str):
        print(external_promise_id)
        if external_promise_id in self.promises:
            client = self.promises[external_promise_id]
            self.server.send_message(client, message)
        else:
            self.server.send_message_to_all(message)

    def parse_message(self, client, message: str):
        obj = json.loads(message)
        type = obj[MESSAGE_TYPE]
        payload = obj[MESSAGE_PAYLOAD]
        external_promise_id = payload[PROMISE_ID_PROPERTY]
        print(external_promise_id)
        self.promises[external_promise_id] = client
        if type in self.handlers:
            self.handlers[type].execute(payload)
