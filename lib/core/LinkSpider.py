#!/usr/bin/env python3
import logging
from lib.var import Config
from html.parser import HTMLParser
from urllib import parse
from urllib import request
from urllib.parse import urlsplit
from urllib.parse import urlparse


class LinkSpider(HTMLParser):
    def __init__(self, url_to_spider):
        HTMLParser.__init__(self)
        self.url = url_to_spider
        self.root = url_to_spider[:url_to_spider.rfind("/") + 1]
        self.absolute_links = []
        self.fileonly_links = []
        self.logger = logging.getLogger("bakspider")

    def get_links(self):
        if Config.is_debug:
            self.logger.info("Harvesting links on: %s", self.url)

        body = request.urlopen(self.url)
        encoding = body.headers.get_content_charset() or "UTF-8"

        try:
            for line in body:
                self.feed(line.decode(encoding))
        except UnicodeDecodeError:
            pass

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    abs_url = self.get_absolute_url(value)
                    file_url = self.get_file_only_url(abs_url)

                    self.absolute_links.append(abs_url)
                    self.fileonly_links.append(file_url)
        return

    def get_absolute_url(self, link):
        # TODO: Maybe consolidate these if-statements, will have to calculate performance.
        if "://" in link:  # Check if relative or absolute
            if link.startswith("{0.scheme}://{0.netloc}/".format(urlsplit(self.root))):
                return link
        else:
            url = parse.urljoin(self.root, link)
            return url

    @staticmethod
    def get_file_only_url(url):
        parsed_url = urlparse(url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

        return clean_url
