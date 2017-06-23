#!/usr/bin/env python3
import os
import logging
from multiprocessing.pool import ThreadPool
from urllib import parse
import lib.utils.WebUtils as WebUtils
from lib.utils.Output import Output


class BackupScanner:
    def __init__(self, fileonly_url, backup_exts, output, thread_count):
        self.url = fileonly_url
        self.backup_extensions = backup_exts
        self.output = output
        self.thread_count = thread_count
        self.logger = logging.getLogger("bakspider")

        self.backup_urls = []

    def begin_scan(self, found_dirs=None):
        self.prepare_for_check(self.url)

        if found_dirs:
            filename = os.path.basename(self.url)

            for dir_path in found_dirs:
                dir_url = parse.urljoin(dir_path, filename)
                self.prepare_for_check(dir_url)

        self.check_for_backups()

    def prepare_for_check(self, url):
        # Check with the original extension
        for ext in self.backup_extensions:
            self.backup_urls.append("{0}{1}".format(url, ext))

        # Check without the original extension
        url = url.rsplit('.', 1)[0]
        for ext in self.backup_extensions:
            self.backup_urls.append("{0}{1}".format(url, ext))

    def check_for_backups(self):
        thread_pool = ThreadPool(int(self.thread_count))
        thread_pool.map(self.check_for_backups_threaded, self.backup_urls)
        thread_pool.close()
        thread_pool.join()

    @staticmethod
    def check_for_backups_threaded(url):
        if WebUtils.is_200_response(url):
            output = Output()
            output.page_found("Backup found: {0}".format(url), True)