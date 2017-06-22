#!/usr/bin/env python3
import os
import logging
from functools import partial
from itertools import repeat
from multiprocessing import Pool
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

    def begin_scan(self, found_dirs=None):
        self.check_for_backups(self.url)

        if found_dirs:
            filename = os.path.basename(self.url)

            self.logger.info("Checking found directories for: %s", filename)

            for dir_path in found_dirs:
                dir_url = parse.urljoin(dir_path, filename)
                self.check_for_backups(dir_url)

    def check_for_backups(self, url):
        backup_urls = []
        # Check with the original extension
        for ext in self.backup_extensions:
            backup_urls.append("{0}{1}".format(url, ext))

        # Check without the original extension
        url = url.rsplit('.', 1)[0]
        for ext in self.backup_extensions:
            backup_urls.append("{0}{1}".format(url, ext))

        thread_pool = Pool(int(self.thread_count))
        thread_pool.map(self.check_for_backups_threaded, backup_urls)
        thread_pool.close()
        thread_pool.join()

    @staticmethod
    def check_for_backups_threaded(url):
        if WebUtils.is_200_response(url):
            output = Output()
            output.page_found("Backup found: {0}".format(url), True)