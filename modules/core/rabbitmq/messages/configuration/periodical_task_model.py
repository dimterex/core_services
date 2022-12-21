PERIODICAL_TASK_MODEL_NAME = 'name'
PERIODICAL_TASK_MODEL_TRACKER_ID = 'trackerId'
PERIODICAL_TASK_MODEL_TRACKER_DURATION = 'duration'


class PeriodicalTaskModel:
    def __init__(self, name: str, tracker_id: str, duration: float):
        self.name = name
        self.tracker_id = tracker_id
        self.duration = duration

    def serialize(self) -> dict:
        return {
            PERIODICAL_TASK_MODEL_NAME: self.name,
            PERIODICAL_TASK_MODEL_TRACKER_ID: self.tracker_id,
            PERIODICAL_TASK_MODEL_TRACKER_DURATION: self.duration,
        }

    @staticmethod
    def deserialize(payload):
        name = payload[PERIODICAL_TASK_MODEL_NAME]
        tracker_id = payload[PERIODICAL_TASK_MODEL_TRACKER_ID]
        duration = payload[PERIODICAL_TASK_MODEL_TRACKER_DURATION]
        return PeriodicalTaskModel(name, tracker_id, duration)

