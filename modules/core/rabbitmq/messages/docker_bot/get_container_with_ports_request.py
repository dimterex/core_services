from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_CONTAINERS_WITH_PORTS_REQUEST_MESSAGE_TYPE = 'get_container_with_ports_request'


class GetContainerWithPortsRequest(BaseMessage):

    def __init__(self):
        super().__init__(GET_CONTAINERS_WITH_PORTS_REQUEST_MESSAGE_TYPE)

    def serialize(self) -> dict:
        return self.to_json(None)
