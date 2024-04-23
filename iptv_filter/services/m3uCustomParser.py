import re
import urllib.request

from iptv_filter.models.ExtM3uHeader import ExtM3uHeader
from iptv_filter.models.ExtM3uInformation import ExtM3uInformation
from iptv_filter.services.linkCheckerService import LinkCheckerService


class M3uParser:
    def __init__(self, url: str, link_checker: LinkCheckerService):
        self.link_checker = link_checker
        self.channels: [ExtM3uInformation] = []
        self.channel_black_list = []
        self.category_black_list = []
        with urllib.request.urlopen(url) as response:
            content = response.read()
            self.content = content.decode("utf-8")

        self.parse()

    def parse(self):
        lines = self.content.splitlines()
        numLine = len(lines)
        for n in range(numLine):
            lineInfo = lines[n]
            if lineInfo.startswith("#"):
                lineLink = lines[n + 1]
                extvcopt = None
                if lineLink.startswith("#"):
                    extvcopt = lines[n + 1]
                    lineLink = lines[n + 2]
                self.manageLine(lineInfo, lineLink, extvcopt)

    def manageLine(self, lineInfo, lineLink, extvcopt):
        if lineInfo.startswith('#EXTVLCOPT'):
            return
        if lineInfo.startswith("#EXTM3U"):
            url_tvg_raw = self.checkRegex("url-tvg=\"(.*?)\"", lineInfo)
            tvg_shift = self.checkRegex("tvg-shift=\"(.*?)\"", lineInfo)
            abs = self.checkRegex("abs=\"(.*?)\"", lineInfo)
            self.header = ExtM3uHeader()
            self.header.url_tvg = url_tvg_raw
        else:
            if lineLink == '':
                return
            name = self.checkRegex("tvg-name=\"(.*?)\"", lineInfo)
            id = self.checkRegex("tvg-ID=\"(.*?)\"", lineInfo)
            logo = self.checkRegex("tvg-logo=\"(.*?)\"", lineInfo)
            group = self.checkRegex("group-title=\"(.*?)\"", lineInfo)
            title = self.checkRegex("[,](?!.*[,])(.*?)$", lineInfo)
            if title.startswith(' '):
                title = title[1:]
            if title.endswith(' '):
                title = title[:-1]

            inf = ExtM3uInformation(title, name, id, logo, group, lineLink, extvcopt)
            self.channels.append(inf)

    def checkRegex(self, regex_value: str, line: str):
        m = re.search(regex_value, line)
        if m:
            return m.group(1)
        else:
            return None

