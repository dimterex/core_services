CONTAINER_MODEL_ID_PROPERTY = 'id'
CONTAINER_MODEL_NAME_PROPERTY = 'name'
CONTAINER_MODEL_PORTS_PROPERTY = 'ports'


class ContainerModel:
    def __init__(self, id: str, name: str, ports: [int]):
        self.ports = ports
        self.name = name
        self.id = id

    def serialize(self):
        return {
            CONTAINER_MODEL_ID_PROPERTY: self.id,
            CONTAINER_MODEL_NAME_PROPERTY: self.name,
            CONTAINER_MODEL_PORTS_PROPERTY: self.ports,
        }

    @staticmethod
    def deserialize(payload):
        name = payload[CONTAINER_MODEL_NAME_PROPERTY]
        id = payload[CONTAINER_MODEL_ID_PROPERTY]
        ports = payload[CONTAINER_MODEL_PORTS_PROPERTY]
        return ContainerModel(id, name, ports)

