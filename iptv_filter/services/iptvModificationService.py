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

    def run(self, sources: [], black_list: [IptvBlackListItemModel], epgs: [str]):
        epgService = EpgService(self.logger_Service, self.iptv_epg_path, self.timezone, epgs)
        playlistService = PlaylistService(self.logger_Service, self.iptv_playlist_path, sources, black_list, self.playlistM3uHeader)

        epgService.update([item.title for item in playlistService.channel_list])

        playlistService.save()
        epgService.save()
