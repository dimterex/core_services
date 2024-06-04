from iptv_filter.models.epg.EpgService import EpgService
from iptv_filter.models.playlist.PlaylistM3uHeader import PlaylistM3uHeader
from iptv_filter.models.playlist.PlaylistService import PlaylistService
from core.log_service.log_service import Logger_Service

from core.rabbitmq.messages.configuration.iptv_black_list_item_model import IptvBlackListItemModel


class IptvModificationService:
    def __init__(self,
                 logger_Service: Logger_Service,
                 iptv_playlist_path: str,
                 iptv_epg_path: str,
                 timezone: int,
                 epg_url: str):

        self.iptv_playlist_path = iptv_playlist_path
        self.iptv_epg_path = iptv_epg_path
        self.logger_Service = logger_Service
        self.TAG = self.__class__.__name__
        self.timezone = timezone
        self.playlistM3uHeader = PlaylistM3uHeader(epg_url)
        self.last_channel_list: [str] = []

    def run(self, sources: [], duplicate_sources, black_list: [IptvBlackListItemModel], epgs: [str]):
        epgService = EpgService(self.logger_Service, self.iptv_epg_path, self.timezone, epgs)
        playlistService = PlaylistService(self.logger_Service, self.iptv_playlist_path, sources, duplicate_sources, black_list, self.playlistM3uHeader)

        channel_names = [item.title for item in playlistService.channel_list]
        epgService.update(channel_names)
        self.show_diff(channel_names)

        playlistService.save()
        epgService.save()

    def show_diff(self, channel_names: [str]):
        removed_items = [channel_name for channel_name in self.last_channel_list if channel_name not in channel_names]
        added_items = [channel_name for channel_name in channel_names if channel_name not in self.last_channel_list]
        self.logger_Service.info(self.TAG, "Удалено:")
        self.logger_Service.info(self.TAG, removed_items)
        self.logger_Service.info(self.TAG, "Добавлено:")
        self.logger_Service.info(self.TAG, added_items)
        self.last_channel_list = channel_names
