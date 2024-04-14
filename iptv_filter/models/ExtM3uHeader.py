class ExtM3uHeader:
    def __init__(self):
        self.abs = 'true'
        self.tvg_shift = '+7'
        self.url_tvg = [
            'http://epg.one/epg2.xml.gz',
            'http://epg.one/ru2.xml.gz',
        ]

    def toRaw(self):
        return [
            f'#EXTM3U url-tvg="{",".join(self.url_tvg)}" tvg-shift="{self.tvg_shift}" abs="{self.abs}"',
            ''
        ]
