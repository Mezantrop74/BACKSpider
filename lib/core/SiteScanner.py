#!/usr/bin/env python3
from multiprocessing import Pool
from lib.core import LinkSpider
from lib.var import Config
from lib.core import BackupScanner


class SiteScanner:
    def __init__(self, url):
        self.url = url
        self.links_to_spider = []
        self.links_to_bak_check = []
        self.additional_dirs = []
        self.backup_extensions = []

        self.spidered_links = []
        self.checked_files = []

    def begin_scan(self):
        page_links = LinkSpider(self.url)
        page_links.get_links()
        self.links_to_spider = page_links.absolute_links
        self.links_to_bak_check = page_links.fileonly_links

        while len(self.links_to_spider) > 0 or len(self.links_to_bak_check) > 0:
            if len(self.links_to_spider) > 0:
                spider_link = self.links_to_spider.pop()

                if spider_link not in self.spidered_links:
                    self.spider_link(spider_link)
                    self.spidered_links.append(spider_link)

            if len(self.links_to_bak_check) > 0:
                backup_link = self.links_to_bak_check.pop()

                if backup_link not in self.checked_files:
                    self.backup_check(backup_link)
                    self.checked_files.append(backup_link)

    def spider_link(self, url):
        if Config.is_debug:
            print("[DEBUG] Spidering:", url)

        spider = LinkSpider(url)
        spider.get_links()

        self.links_to_spider = self.links_to_spider + spider.absolute_links
        self.links_to_bak_check = self.links_to_bak_check + spider.fileonly_links

    def backup_check(self, fileonly_url):
        if Config.is_debug:
            print("[DEBUG] Backup check:", fileonly_url)

        check = BackupScanner(fileonly_url, self.backup_extensions)

        if self.additional_dirs:
            check.begin_scan(self.additional_dirs)
        else:
            check.begin_scan()

        del check




