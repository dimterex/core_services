import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, QUEUE_RESPOND, MESSAGE_TYPE, \
    MESSAGE_PAYLOAD

UPDATE_LABEL_MESSAGE_TYPE = 'update_label_request'
UPDATE_LABEL_TODOIST_TASK_ID = 'id'
UPDATE_LABEL_TODOIST_TASK_LABEL = 'label'


class UpdateLabelRequest:
    def __init__(self, id: str, label: str):
        self.label = label
        self.id = id

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: UPDATE_LABEL_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                UPDATE_LABEL_TODOIST_TASK_ID: self.id,
                UPDATE_LABEL_TODOIST_TASK_LABEL: self.label,
            }
        }
        return json.dumps(dict_object)
