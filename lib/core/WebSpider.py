#!/usr/bin/env python3
import os
from html.parser import HTMLParser
from urllib import parse
from urllib import request
from urllib.parse import urlsplit
from urllib.parse import urlparse
from lib.core import Util

spidered_links = []

class WebSpider(HTMLParser):
    """Class to help with our webpage operations."""
    # TODO: Calculate root rather than have it passed.
    # TODO: Remove the recursive functionality, one scan per class instance.
    # TODO: Don't pass whole argparse object
    def __init__(self, url, root, args, additional_dirs=None):
        HTMLParser.__init__(self)
        self.args = args
        self.url = url
        self.root = root
        self.additional_dirs = additional_dirs
        self.backup_extensions = Util.read_file_into_array(args.ext)
        return

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.parse_href(value)
        return

    def parse_href(self, link):
        # TODO: Maybe consolidate these if-statements, will have to calculate performance.
        if "://" in link:  # Check if relative or absolute
            if link.startswith("{0.scheme}://{0.netloc}/".format(urlsplit(self.root))):
                self.parse_url(link)
        else:
            url = parse.urljoin(self.root, link)
            self.parse_url(url)

        return

    def parse_url(self, url):
        parsed_url = urlparse(url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

        self.spider_url(url, clean_url)
        return

    def spider_url(self, url_to_spider, file_only_url):
        if not Util.is_valid_url(file_only_url):
            return

        checked_files = []

        if file_only_url not in checked_files and not file_only_url.endswith('/'):
            # Check for backups here
            print("Checking {0} for backups now:".format(file_only_url))
            self.check_url(file_only_url)
            self.check_dirs_for_backups(file_only_url)  # TODO: Enable this if directory scanning is enabled.

            checked_files.append(file_only_url)

        if url_to_spider not in spidered_links:
            root = url_to_spider[:url_to_spider.rfind("/") + 1]

            # Begin spidering a new page
            spidered_links.append(url_to_spider)
            WebSpider(url_to_spider, root, self.args).scan()
        return

    # TODO: Check for certain extensions (exclude PDF etc.)
    # TODO: This is still being called when the --dir option isn't specified
    def check_dirs_for_backups(self, url):
        filename = os.path.basename(url)
        print("Checking dirs for", filename)

        for dir_name in self.additional_dirs:
            dir_url = parse.urljoin(dir_name, filename)
            self.check_url(dir_url)

    def check_url(self, url):
        # Check with original extension
        for ext in self.backup_extensions:
            bak_url = "{0}.{1}".format(url, ext)
            print(bak_url)

            if Util.is_200_response(bak_url):
                print("[200 - OK] Backup found: {0}".format(bak_url))

        # Check without original extension
        url = url.rsplit('.', 1)[0]
        for ext in self.backup_extensions:
            bak_url = "{0}.{1}".format(url, ext)
            print(bak_url)

            if Util.is_200_response(bak_url):
                print("[200 - OK] Backup found: {0}".format(bak_url))

    def scan(self):
        print("---###[ SCANNING {0} ]###---".format(self.url))

        body = request.urlopen(self.url)
        page_enc = body.headers.get_content_charset() or 'UTF-8'

        try:
            for line in body:
                self.feed(line.decode(page_enc))
        except UnicodeDecodeError:
            pass
