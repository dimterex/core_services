CATEGORY_MODEL_ID = 'id'
CATEGORY_MODEL_NAME = 'name'
CATEGORY_MODEL_TRACKER_ID = 'trackerId'
CATEGORY_MODEL_TRACKER_LINK = 'link'


class CategoryModel:
    def __init__(self, id: int, name: str, tracker_id: str, link: str):
        self.id = id
        self.name = name
        self.tracker_id = tracker_id
        self.link = link

    def serialize(self) -> dict:
        return {
            CATEGORY_MODEL_ID: self.id,
            CATEGORY_MODEL_NAME: self.name,
            CATEGORY_MODEL_TRACKER_ID: self.tracker_id,
            CATEGORY_MODEL_TRACKER_LINK: self.link,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[CATEGORY_MODEL_ID]
        name = payload[CATEGORY_MODEL_NAME]
        tracker_id = payload[CATEGORY_MODEL_TRACKER_ID]
        link = payload[CATEGORY_MODEL_TRACKER_LINK]
        return CategoryModel(id, name, tracker_id, link)

