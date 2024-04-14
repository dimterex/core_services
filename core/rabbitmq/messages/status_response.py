from core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

STATUS_RESPONSE_TYPE = 'status_response_type'
STATUS_RESPONSE_MESSAGE_PROPERTY = 'message'
STATUS_RESPONSE_STATUS_PROPERTY = 'status'

SUCCESS_STATUS_CODE = 'ok'
ERROR_STATUS_CODE = 'error'


class StatusResponse:
    def __init__(self, message: object, status: str = SUCCESS_STATUS_CODE):
        self.status = status
        self.message = message

    def serialize(self) -> dict:
        return {
            MESSAGE_TYPE: STATUS_RESPONSE_TYPE,
            MESSAGE_PAYLOAD: {
                STATUS_RESPONSE_MESSAGE_PROPERTY: self.message,
                STATUS_RESPONSE_STATUS_PROPERTY: self.status,
            }
        }

    @staticmethod
    def deserialize(json_dct):
        payload = json_dct[MESSAGE_PAYLOAD]
        status = payload[STATUS_RESPONSE_STATUS_PROPERTY]
        message = payload[STATUS_RESPONSE_MESSAGE_PROPERTY]
        return StatusResponse(message, status)
