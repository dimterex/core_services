import os


class TrackStorageDto:
    def __init__(self, track_path: str, track_name: str):
        self.cover_path = os.path.join(track_path, f'{track_name}.png')
        self.file_path = os.path.join(track_path, f'{track_name}.mp3')
        self.track_name = track_name
