from core.log_service.log_service import Logger_Service
from iptv_filter.models.epg.EpgParser import EpgParser


class EpgService:
    def __init__(self, logger_Service: Logger_Service, iptv_epg_path: str, timezone: int, epgs: [str]):
        self.logger_Service = logger_Service
        self.tv_programs = []
        self.tv_program_channels = {}
        self.epgs: [str] = []
        self.timezone = timezone
        self.TAG = self.__class__.__name__
        self.iptv_epg_path = iptv_epg_path

        self.epgs: [str] = epgs

    def update(self, channel_names: [str]):
        for epg in self.epgs:
            channels, programs = EpgParser(channel_names, self.timezone).parse_xmltv(epg)

            names = [channels[item].display_name for item in channels]
            self.logger_Service.info(self.TAG, f'TV channels {epg}: {len(names)}.')
            self.logger_Service.info(self.TAG, f'TV channels {"; ".join(names)}.')
            self.tv_programs += programs
            self.tv_program_channels.update(channels)

    def save(self):
        with open(self.iptv_epg_path, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8" ?><!DOCTYPE tv SYSTEM "http://127.0.0.1">\n')
            file.write('<tv>\n')
            for channel_id in self.tv_program_channels:
                tv_channel = self.tv_program_channels[channel_id]
                file.write("%s\n" % tv_channel.toRaw())

            for tv_program in self.tv_programs:
                file.write("%s\n" % tv_program.toRaw())

            file.write('</tv>')
        self.logger_Service.info(self.TAG, f'TV program updated.')

