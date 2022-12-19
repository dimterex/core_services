import json

from modules.core.rabbitmq.messages.base_request import BaseMessage
from modules.core.rabbitmq.messages.identificators import MESSAGE_TYPE, \
    MESSAGE_PAYLOAD

UPDATE_LABEL_MESSAGE_TYPE = 'update_label_request'
UPDATE_LABEL_TODOIST_TASK_ID = 'id'
UPDATE_LABEL_TODOIST_TASK_LABEL = 'label'


class UpdateLabelRequest(BaseMessage):

    def __init__(self, id: str, label: str):
        super().__init__(UPDATE_LABEL_MESSAGE_TYPE)
        self.label = label
        self.id = id

    def serialize(self) -> dict:
        return self.to_json({
            UPDATE_LABEL_TODOIST_TASK_ID: self.id,
            UPDATE_LABEL_TODOIST_TASK_LABEL: self.label,
        })
