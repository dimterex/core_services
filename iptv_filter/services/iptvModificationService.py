import re

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
        self.last_channel_list: [ExtM3uInformation] = []
        self.channel_list: [ExtM3uInformation] = []
        self.m3uParsers: [M3uParser] = []

    def initialize(self, sources: []):
        self.channel_list: [ExtM3uInformation] = []
        for url in sources:
            parser = M3uParser(url, self.link_checker)
            self.channel_list += parser.channels
        self.remove_duplicates()

    def remove_duplicates(self):
        title_dict = {}
        for channel in self.channel_list:
            title = channel.title.lower()
            if title not in title_dict:
                title_dict[title] = channel

        sorted_dict = dict(sorted(title_dict.items()))

        self.channel_list = list(sorted_dict.values())

    def remove(self, channels: [ExtM3uInformation]):
        for channel in channels:
            self.channel_list.remove(channel)

    def remove_categories(self, category_black_list: [str]):
        removed = []
        for channel in self.channel_list:
            if channel.group in category_black_list:
                removed.append(channel)
        self.remove(removed)

    def remove_regex(self, regex_black_list: [str]):
        removed = []
        for channel in self.channel_list:
            for regex_value in regex_black_list:
                m = re.search(regex_value, channel.raw_title)
                if m:
                    removed.append(channel)
        self.remove(removed)

    def remove_channels(self, channels_black_list: [str]):
        removed = []
        for channel in self.channel_list:
            if channel.title.lower() in channels_black_list:
                removed.append(channel)
        self.remove(removed)

    def remove_unworking(self):
        removed = []
        for channel in self.channel_list:
            if not self.link_checker.check(channel.link):
                removed.append(channel)
        self.remove(removed)

    def apply(self):
        removed_items = [item.title for item in self.last_channel_list if item not in self.channel_list]
        added_items = [item.title for item in self.channel_list if item not in self.last_channel_list]
        self.logger_Service.info(self.TAG, "Удалено:")
        self.logger_Service.info(self.TAG, removed_items)
        self.logger_Service.info(self.TAG, "Добавлено:")
        self.logger_Service.info(self.TAG, added_items)
        self.last_channel_list = self.channel_list

    def saveFile(self):
        with open(self.iptv_playlist_path, 'w', encoding='utf-8') as file:
            for item in self.header.toRaw():
                file.write("%s\n" % item)

            for channel in self.channel_list:
                for item in channel.toRaw():
                    file.write("%s\n" % item)
                # self.logger_Service.trace(self.TAG, f'{channel.title}; group: {channel.group};')
        self.logger_Service.info(self.TAG, f'Saved {len(self.channel_list)} channels.')
