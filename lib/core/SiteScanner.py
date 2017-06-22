#!/usr/bin/env python3
import logging
from datetime import datetime
from lib.core import LinkSpider
from lib.core import BackupScanner
import lib.utils.WebUtils as WebUtils


class SiteScanner:
    def __init__(self, url, output, thread_count):
        self.url = url
        self.output = output
        self.thread_count = thread_count
        self.links_to_spider = []
        self.links_to_bak_check = []
        self.additional_dirs = []
        self.backup_extensions = []
        self.whitelist_extensions = []

        self.spidered_links = []
        self.checked_files = []

        self.logger = logging.getLogger("bakspider")

    def begin_scan(self):
        # Start timer
        start_time = datetime.now()
        self.output.progress("Starting backup scan at: {0}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

        # Start main scanning logic.
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

        self.output.status("Backup scan completed at: {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.output.status("Time elapsed: {0}".format((datetime.now() - start_time)))

    def spider_link(self, url):
        self.logger.info("Spidering url: %s", url)

        if not WebUtils.is_valid_url(url):
            return

        spider = LinkSpider(url)
        spider.get_links()

        self.links_to_spider = self.links_to_spider + spider.absolute_links
        self.links_to_bak_check = self.links_to_bak_check + spider.fileonly_links

    def backup_check(self, fileonly_url):
        url_ext = WebUtils.get_url_extension(fileonly_url)

        if url_ext not in self.whitelist_extensions:
            self.logger.info("This URL has no extension or it isn't in the whitelist. [{0}]".format(fileonly_url))
            return

        self.logger.info("Searching for backup files: %s", fileonly_url)

        check = BackupScanner(fileonly_url, self.backup_extensions, self.output, self.thread_count)

        if self.additional_dirs:
            check.begin_scan(self.additional_dirs)
        else:
            check.begin_scan()
