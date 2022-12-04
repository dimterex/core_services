import json


class LogModel:
    def __init__(self, application_name: str, tag: str, level: str, datetime: str, message: str):
        self.message = message
        self.datetime = datetime
        self.level = level
        self.tag = tag
        self.applicationName = application_name

    def to_json(self):
        dict_object = {
            'message': self.message,
            'datetime': self.datetime,
            'level': self.level,
            'tag': self.tag,
            'applicationName': self.applicationName
        }
        return json.dumps(dict_object)
        