from yandex_music import Track


class TrackDto:
    def __init__(self, track: Track):
        self.id = track.id
        self.artists = ', '.join(track.artists_name())
        self.albums = track.albums[0].title
        self.album_artists = ', '.join([i.name for i in track.albums[0].artists])
        self.year = str(track.albums[0].year)
        self.track_position = track.albums[0].track_position.index
        self.album_tracks = track.albums[0].track_count
        self.title = track.title
