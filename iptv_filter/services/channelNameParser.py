class ChannelNameParser:

    def __init__(self):
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
            'UK',
            'HD 50 UK',
            'SE',
            'HD (Sky) DE',
            'HD US',
            'RO',
            'FHD UK',
            'DE',
        ]

    def parse(self, input_title):
            for supported_format in self.supported_formats:
                if supported_format in input_title:
                    channel_name = input_title.split(supported_format)[0]
                    if channel_name.endswith('('):
                        channel_name = channel_name[:-1]
                    if channel_name.endswith(' '):
                        channel_name = channel_name[:-1]
                    return channel_name, supported_format
            return input_title, None