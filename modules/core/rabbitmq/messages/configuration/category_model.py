CATEGORY_MODEL_NAME = 'name'
CATEGORY_MODEL_TRACKER_ID = 'trackerId'
CATEGORY_MODEL_TRACKER_LINK = 'link'


class CategoryModel:
    def __init__(self, name: str, tracker_id: str, link: str):
        self.name = name
        self.tracker_id = tracker_id
        self.link = link

    def serialize(self) -> dict:
        return {
            CATEGORY_MODEL_NAME: self.name,
            CATEGORY_MODEL_TRACKER_ID: self.tracker_id,
            CATEGORY_MODEL_TRACKER_LINK: self.link,
        }

    @staticmethod
    def deserialize(payload):
        name = payload[CATEGORY_MODEL_NAME]
        tracker_id = payload[CATEGORY_MODEL_TRACKER_ID]
        link = payload[CATEGORY_MODEL_TRACKER_LINK]
        return CategoryModel(name, tracker_id, link)

