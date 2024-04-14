import docker

from docker_bot.models.container_model import ContainerModel
from core.rabbitmq.messages.docker_bot.get_container_with_ports_request import \
    GET_CONTAINERS_WITH_PORTS_REQUEST_MESSAGE_TYPE
from core.rabbitmq.messages.status_response import StatusResponse
from core.rabbitmq.rpc.rpc_base_handler import RpcBaseHandler


class GetContainerWithPortsRequestHandler(RpcBaseHandler):
    def __init__(self):
        super().__init__(GET_CONTAINERS_WITH_PORTS_REQUEST_MESSAGE_TYPE)
        self.TAG = self.__class__.__name__

    def execute(self, payload) -> StatusResponse:
        client = docker.from_env()
        containers: list[ContainerModel] = []
        for c in client.containers.list(all=True):
            ports: list[int] = []
            for portParams in c.ports:
                raw_ports = c.ports[portParams]
                if raw_ports is None:
                    continue
                for raw_port in raw_ports:
                    port = raw_port["HostPort"]
                    if int(port) not in ports:
                        ports.append(int(port))

            containers.append(ContainerModel(c.id, c.name, ports).serialize())
        return StatusResponse(containers)
