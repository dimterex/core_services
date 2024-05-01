class PlaylistM3uHeader:
    def __init__(self, url_tvg: str):
        self.url_tvg = url_tvg

    def toRaw(self):
        return [
            f'#EXTM3U url-tvg="{",".join(self.url_tvg)}"',
            ''
        ]
