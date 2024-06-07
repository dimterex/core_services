import gzip
import os
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from iptv_filter.models.epg.EpgChannel import EpgChannel
from iptv_filter.models.epg.EpgProgram import EpgProgram
from iptv_filter.services.channelNameParser import ChannelNameParser


class EpgParser:

    def __init__(self, channels: [str], timezone: int):
        self.timezone = timezone
        self.channels = channels
        self.channelNameParser = ChannelNameParser()

    def unzip_gz_file(self, gz_file_path):
        unzipped_file_path = os.path.splitext(gz_file_path)[0]
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(unzipped_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        return unzipped_file_path

    def download(self, url):
        filename = os.path.join(url.split('/')[-1])
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)

        return filename

    def parse_xmltv(self, url):
        filename = self.download(url)
        unzipped_file_path = self.unzip_gz_file(filename)

        channels = {}
        programs = []

        tree = ET.parse(unzipped_file_path)
        root = tree.getroot()

        for channel_elem in root.findall('.//channel'):
            channel_id = channel_elem.get('id')
            display_names = channel_elem.findall('display-name')

            display_name = None
            for epg_channel_name in display_names:
                channel_name, channel_format = self.channelNameParser.parse(epg_channel_name.text)
                if channel_name.lower() in self.channels:
                    display_name = channel_name
                    break

            if display_name is None:
                continue

            icon = channel_elem.find('icon').get('src')
            channels[channel_id] = EpgChannel(channel_id, display_name, icon)

        for program_elem in root.findall('.//programme'):
            start_time = program_elem.get('start')
            stop_time = program_elem.get('stop')
            channel_id = program_elem.get('channel')
            if channel_id not in channels:
                continue

            title = program_elem.find('title').text

            desc = program_elem.find('desc')
            description = None
            if desc is not None:
                description = desc.text
            epgProgram = EpgProgram(start_time, stop_time, channel_id, title, description, self.timezone)
            now = datetime.now().date()
            if epgProgram.start_time.date() < now or epgProgram.stop_time.date() < now:
                continue
            programs.append(epgProgram)

        os.remove(filename)
        os.remove(unzipped_file_path)
        return channels, programs
