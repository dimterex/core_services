import json

from modules.models.log_service import Logger_Service, ERROR_LOG_LEVEL, TRACE_LOG_LEVEL


class Api_Controller:

    def __init__(self, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.type_to_queue = []
        self.handlers = []

    def configure(self, queue: str, type: str, callback):
        mapper = None
        if len(self.type_to_queue) != 0:
            for type_queue in self.type_to_queue:
                if type_queue.type == type:
                    mapper = type_queue
                    break

        if mapper is None:
            mapper = Type_To_Queue_Mapper(type, queue)
            self.type_to_queue.append(mapper)

        type_handlers = None
        if len(self.handlers) != 0:
            for x in self.handlers:
                if x.type == type:
                    type_handlers = x
                    break

        if type_handlers is None:
            type_handlers = Type_Handlers(type)
            self.handlers.append(type_handlers)

        type_handlers.add_handler(callback)

    def received(self, message: str):
        if message is None:
            return
        try:
            self.logger_service.send_log(TRACE_LOG_LEVEL, self.__class__.__name__, message)
            obj = json.loads(message)
            type = obj['type']
            payload = obj['value']

            type_handlers = None
            if len(self.handlers) != 0:
                type_handlers = next(x for x in self.handlers if x.type == type)

            if type_handlers is not None:
                type_handlers.execute(payload)
        except Exception as e:
            self.logger_service.send_log(ERROR_LOG_LEVEL, self.__class__.__name__, f'Cant parse message: {e}; \n {message}')


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

