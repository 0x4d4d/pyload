# -*- coding: utf-8 -*-

from module.plugins.internal.MultiHoster import MultiHoster
from module.network.RequestFactory import getURL
from module.common.json_layer import json_loads as loads


class RapideoPl(MultiHoster):
    __name__ = "RapideoPl"
    __version__ = "0.01"
    __type__ = "hook"

    __config__ = [("activated", "bool", "Activated", "False"),
                  ("hosterListMode", "all;listed;unlisted", "Use for hosters (if supported):", "all"),
                  ("hosterList", "str", "Hoster list (comma separated)", ""),
                  ("unloadFailing", "bool", "Try standard download if download fails", "False"),
                  ("interval", "int", "Reload supported hosts interval in hours (0 to disable)", "24")]

    __description__ = "Rapideo.pl hook"
    __author_name__ = ("goddie")
    __author_mail__ = ("dev@rapideo.pl")

    def getHoster(self):
        hostings = loads(getURL("https://www.rapideo.pl/clipboard.php?json=3").strip())

        return [domain for row in hostings for domain in row["domains"] if row["sdownload"] == "0"]

    def getHosterCached(self):
        return self.getHoster()


