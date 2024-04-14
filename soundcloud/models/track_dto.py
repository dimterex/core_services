class TrackDto:
    def __init__(self, dict: {}):
        self.id = dict['id']
        self.url = dict['permalink_url']
        self.dict = dict
