import re


class ExtM3uInformation:
    def __init__(self, title: str, name: str, id: str, logo: str, group: str, link: str, extvcopt: str):
        self.supported_formats = [
            'nHD',
            'SDTV 480i',
            'EDTV 480p',
            '480p',
            'D1',
            '768×432',
            '720×540',
            'SDTV 576i',
            'EDTV 576p',
            'WSVGA',
            'HD ready',
            'HD',
        ]
        self.raw_title = title
        self.name = name
        self.id = id
        self.logo = logo
        self.group = group
        self.link = link
        self.extvcopt = extvcopt
        channel_name, channel_format = self.parseChannelName(title)
        self.channelFormat = channel_format
        self.title = channel_name

    def parseChannelName(self, input_string):
        for supported_format in self.supported_formats:
            if supported_format in input_string:
                channel_name = input_string.split(supported_format)[0]
                if channel_name.endswith('('):
                    channel_name = channel_name[:-1]
                if channel_name.endswith(' '):
                    channel_name = channel_name[:-1]
                return channel_name, supported_format
        return input_string, None

    def toRaw(self):
        result = '#EXTINF:-1'

        result += self.format('tvg-id', self.id)
        result += self.format('tvg-logo', self.logo)
        result += self.format('group-title', self.group)
        result += ', ' + self.title
        # if self.channelFormat is not None:
        #     result += f' {self.channelFormat}'

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
