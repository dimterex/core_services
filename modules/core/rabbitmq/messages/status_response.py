import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

STATUS_RESPONSE_TYPE = 'exception_response_type'
STATUS_RESPONSE_MESSAGE_PROPERTY = 'message'
STATUS_RESPONSE_STATUS_PROPERTY = 'status'

SUCCESS_STATUS_CODE = 'ok'
ERROR_STATUS_CODE = 'error'


class StatusResponse:
    def __init__(self, status=SUCCESS_STATUS_CODE, message=''):
        self.status = status
        self.message = message

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: STATUS_RESPONSE_TYPE,
            MESSAGE_PAYLOAD: {
                STATUS_RESPONSE_MESSAGE_PROPERTY: self.message,
                STATUS_RESPONSE_STATUS_PROPERTY: self.status,
            }
        }
        return json.dumps(dict_object)

