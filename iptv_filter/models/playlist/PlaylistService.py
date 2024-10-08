import re

from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.iptv_black_list_item_model import IptvBlackListItemModel, CATEGORY_TYPE, \
    REGEX_TYPE, CHANNEL_TYPE
from core.rabbitmq.messages.configuration.iptv_duplicate_list_item_model import IptvDuplicateListItemModel
from iptv_filter.models.playlist.PlaylistM3uHeader import PlaylistM3uHeader
from iptv_filter.models.playlist.ExtM3uInformation import ExtM3uInformation
from iptv_filter.services.linkCheckerService import LinkCheckerService
from iptv_filter.services.m3uCustomParser import M3uParser


class PlaylistService:
    def __init__(self,
                 logger_Service: Logger_Service,
                 iptv_playlist_path: str,
                 sources: [],
                 duplicates: [IptvDuplicateListItemModel],
                 black_list: [IptvBlackListItemModel],
                 header: PlaylistM3uHeader):
        self.TAG = self.__class__.__name__
        self.logger_Service = logger_Service
        self.iptv_playlist_path = iptv_playlist_path
        self.header = header

        self.link_checker = LinkCheckerService()
        self.channel_list: [ExtM3uInformation] = []
        self.m3uParsers: [M3uParser] = []
        self.black_list = black_list

        for url in sources:
            parser = M3uParser(url, self.link_checker)
            self.channel_list += parser.channels

        self.logger_Service.info(self.TAG, f'Loaded {len(self.channel_list)} channels.')

        self.remove_duplicates([element for element in duplicates if element.type == CHANNEL_TYPE])
        self.logger_Service.info(self.TAG, f'After remove duplicates {len(self.channel_list)} channels.')

        self.rename_categories([element for element in duplicates if element.type == CATEGORY_TYPE])
        self.logger_Service.info(self.TAG, f'After remove categories {len(self.channel_list)} channels.')

        category_black_list = [element.value for element in black_list if element.type == CATEGORY_TYPE]
        self.remove_categories(category_black_list)
        self.logger_Service.info(self.TAG, f'After remove categories {len(self.channel_list)} channels.')

        regex_black_list = [element.value for element in black_list if element.type == REGEX_TYPE]
        self.remove_regex(regex_black_list)
        self.logger_Service.info(self.TAG, f'After remove regex {len(self.channel_list)} channels.')

        channel_black_list = [element.value.lower() for element in black_list if element.type == CHANNEL_TYPE]
        self.remove_channels(channel_black_list)
        self.logger_Service.info(self.TAG, f'After remove channels {len(self.channel_list)} channels.')

        # self.remove_unworking()

    def rename_categories(self, duplicate_categories: [IptvDuplicateListItemModel]):
        for channel in self.channel_list:
            duplicates = [element for element in duplicate_categories if element.old_value == channel.group]
            if len(duplicates) > 0:
                channel.group = duplicates[0].value

    def remove_duplicates(self, duplicate_channels: [IptvDuplicateListItemModel]):
        title_dict = {}
        for channel in self.channel_list:
            duplicates = [element for element in duplicate_channels if element.old_value == channel.title]
            if len(duplicates) > 0:
                channel.title = duplicates[0].value
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

    def save(self):
        with open(self.iptv_playlist_path, 'w', encoding='utf-8') as file:
            for item in self.header.toRaw():
                file.write("%s\n" % item)

            for channel in self.channel_list:
                for item in channel.toRaw():
                    file.write("%s\n" % item)
                # self.logger_Service.trace(self.TAG, f'{channel.title}; group: {channel.group};')
        self.logger_Service.info(self.TAG, f'Saved {len(self.channel_list)} channels.')
