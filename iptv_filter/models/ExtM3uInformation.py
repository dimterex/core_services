class ExtM3uInformation:
    def __init__(self, title: str, name: str, id: str, logo: str, group: str, link: str, extvcopt: str):
        self.title = title
        self.name = name
        self.id = id
        self.logo = logo
        self.group = group
        self.link = link
        self.extvcopt = extvcopt

    def toRaw(self):
        result = '#EXTINF:-1'

        result += self.format('tvg-id', self.id)
        result += self.format('tvg-logo', self.logo)
        result += self.format('group-title', self.group)
        result += ',' + self.title

        if self.extvcopt is not None:
            result += '\n' + self.extvcopt

        return [
            result,
            self.link
        ]

    def format(self, key, value):
        if value is not None:
            return f' {key}="{value}"'
        return ''