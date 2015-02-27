# _*_ coding: utf-8 _*_

"""
Reference: https://stackoverflow.com/questions/12553117/how-to-filter-duplicate-requests-based-on-url-in-scrapy
"""
import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""

    def __getid(self, url):
        mm = url.split("&refer")[0] #or something like that
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp +
                            os.linesep)




