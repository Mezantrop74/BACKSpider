#!/usr/bin/env python3
import os
import logging
from urllib import parse
from lib.var import Config
import lib.utils.WebUtils as WebUtils


class BackupScanner:
    def __init__(self, fileonly_url, backup_exts, output):
        self.url = fileonly_url
        self.backup_extensions = backup_exts
        self.output = output
        self.logger = logging.getLogger("bakspider")

    def begin_scan(self, found_dirs=None):
        self.check_for_backups(self.url)

        if found_dirs:
            filename = os.path.basename(self.url)

            if Config.is_debug:
                self.logger.info("Checking found directories for: %s", filename)

            for dir_path in found_dirs:
                dir_url = parse.urljoin(dir_path, filename)
                self.check_for_backups(dir_url)

    def check_for_backups(self, url):
        # Check with the original extension
        for ext in self.backup_extensions:
            backup_url = "{0}{1}".format(url, ext)

            if Config.is_debug:
                self.logger.info("Checking: %s", backup_url)

            if WebUtils.is_200_response(backup_url):
                self.output.page_found("Backup found: {0}".format(backup_url), True)

        # Check without the original extension
        url = url.rsplit('.', 1)[0]
        for ext in self.backup_extensions:
            backup_url = "{0}{1}".format(url, ext)

            if Config.is_debug:
                self.logger.info("Checking: %s", backup_url)

            if WebUtils.is_200_response(backup_url):
                self.output.page_found("Backup found: {0}".format(backup_url), True)
