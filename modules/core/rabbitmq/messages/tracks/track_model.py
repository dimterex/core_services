TRACK_MODEL_TITLE = 'title'
TRACK_MODEL_ALBUM = 'albums'
TRACK_MODEL_ARTISTS = 'artists'
TRACK_MODEL_ALBUM_ARTISTS = 'album_artists'
TRACK_MODEL_YEAR = 'year'
TRACK_MODEL_POSITION = 'position'
TRACK_MODEL_TRACKS_COUNT = 'tracks_count'
TRACK_MODEL_COVER = 'cover'


class TrackModel:
    def __init__(self, title: str, albums: str, artists: str, album_artists: str, year: str, position: str, tracks_count: str, cover: str):
        self.title = title
        self.albums = albums
        self.artists = artists
        self.album_artists = album_artists
        self.year = year
        self.position = position
        self.tracks_count = tracks_count
        self.cover = cover

    def serialize(self) -> dict:
        return {
            TRACK_MODEL_TITLE: self.title,
            TRACK_MODEL_ALBUM: self.albums,
            TRACK_MODEL_ARTISTS: self.artists,
            TRACK_MODEL_ALBUM_ARTISTS: self.album_artists,
            TRACK_MODEL_YEAR: self.year,
            TRACK_MODEL_POSITION: self.position,
            TRACK_MODEL_TRACKS_COUNT: self.tracks_count,
            TRACK_MODEL_COVER: self.cover,
        }

    @staticmethod
    def deserialize(payload):
        title = payload[TRACK_MODEL_TITLE]
        albums = payload[TRACK_MODEL_ALBUM]
        artists = payload[TRACK_MODEL_ARTISTS]
        album_artists = payload[TRACK_MODEL_ALBUM_ARTISTS]
        year = payload[TRACK_MODEL_YEAR]
        position = payload[TRACK_MODEL_POSITION]
        tracks_count = payload[TRACK_MODEL_TRACKS_COUNT]
        cover = payload[TRACK_MODEL_COVER]
        return TrackModel(title, albums, artists, album_artists, year, position, tracks_count, cover)
