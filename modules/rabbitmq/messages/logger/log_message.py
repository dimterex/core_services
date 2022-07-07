import json

from modules.rabbitmq.messages.identificators import LOGGER_MESSAGE_TYPE, LOGGER_MESSAGE_LEVEL, LOGGER_MESSAGE_TAG, \
    LOGGER_MESSAGE_APPLICATION, LOGGER_MESSAGE_DATETIME, LOGGER_MESSAGE_MESSAGE


class Log_Message:
    def __init__(self, applicationName: str, tag: str, level: str, datetime: str, message: str):
        self.message = message
        self.datetime = datetime
        self.level = level
        self.tag = tag
        self.applicationName = applicationName

    def to_json(self):
        dict_object = {
            'type': LOGGER_MESSAGE_TYPE,
            'value': {
                LOGGER_MESSAGE_LEVEL: self.level,
                LOGGER_MESSAGE_TAG: self.tag,
                LOGGER_MESSAGE_APPLICATION: self.applicationName,
                LOGGER_MESSAGE_DATETIME: self.datetime,
                LOGGER_MESSAGE_MESSAGE: self.message
            }
        }
        return json.dumps(dict_object)
