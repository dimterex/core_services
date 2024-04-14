from iptv_filter.models.ExtM3uHeader import ExtM3uHeader
from iptv_filter.models.ExtM3uInformation import ExtM3uInformation
from iptv_filter.services.linkCheckerService import LinkCheckerService
from iptv_filter.services.m3uCustomParser import M3uParser
from core.log_service.log_service import Logger_Service


class IptvModificationService:
    def __init__(self, logger_Service: Logger_Service, iptv_playlist_path: str):
        self.iptv_playlist_path = iptv_playlist_path
        self.logger_Service = logger_Service
        self.TAG = self.__class__.__name__
        self.header = ExtM3uHeader()
        self.link_checker = LinkCheckerService()

    def parse(self, urls: [str], channel_black_list: [str], category_black_list: [str]):
        channels: [ExtM3uInformation] = []
        for url in urls:
            parser = M3uParser(url, channel_black_list, category_black_list, self.link_checker)
            parser.parse()
            channels += parser.channels

        self.saveFile(self.iptv_playlist_path, channels)
        self.logger_Service.info(self.TAG, f'Saved {len(channels)} channels.')

    def saveFile(self, filepath: str, channels):
        with open(filepath, 'w', encoding='utf-8') as file:
            for item in self.header.toRaw():
                file.write("%s\n" % item)

            for channel in channels:
                for item in channel.toRaw():
                    file.write("%s\n" % item)
