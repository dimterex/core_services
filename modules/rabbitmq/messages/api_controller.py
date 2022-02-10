import json


class Api_Controller:

    def __init__(self):
        self.type_to_queue = []
        self.handlers = []

    def configure(self, queue: str, type: str, callback):
        mapper = None
        if len(self.type_to_queue) != 0:
            mapper = next(x for x in self.type_to_queue if x.type == type)

        if mapper is None:
            mapper = Type_To_Queue_Mapper(type, queue)
            self.type_to_queue.append(mapper)

        type_handlers = None
        if len(self.handlers) != 0:
            type_handlers = next(x for x in self.handlers if x.type == type)
        if type_handlers is None:
            type_handlers = Type_Handlers(type)
            self.handlers.append(type_handlers)

        type_handlers.add_handler(callback)

    def receaved(self, message: str):
        if message is None:
            return
        obj = json.loads(message)
        type = obj['type']
        payload = obj['value']

        type_handlers = None
        if len(self.handlers) != 0:
            type_handlers = next(x for x in self.handlers if x.type == type)

        if type_handlers is not None:
            type_handlers.execute(payload)


class Type_To_Queue_Mapper:
    def __init__(self, type: str, queue: str):
        self.queue = queue
        self.type = type


class Type_Handlers:
    def __init__(self, type: str):
        self.type = type
        self.actions = []

    def add_handler(self, handler):
        self.actions.append(handler)

    def execute(self, payload):
        for action in self.actions:
            action(payload)

