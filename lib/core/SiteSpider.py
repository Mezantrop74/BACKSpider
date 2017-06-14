#!/usr/bin/env python3
import os
from html.parser import HTMLParser
from urllib import parse
from urllib import request
from urllib.parse import urlsplit
from urllib.parse import urlparse
from lib.core import Util
from lib.core import DirScanner


class SiteSpider(HTMLParser):
    """Class to help with our website operations."""
    # TODO: Don't pass whole argparse object
    def __init__(self, args):
        HTMLParser.__init__(self)
        self.spidered_links = []
        self.checked_files = []
        self.args = args
        self.root = args.url
        self.backup_extensions = Util.read_file_into_array(args.ext)

        if args.dir:
            self.additional_dirs = DirScanner.scan(args.url, args.dir, args.threads)
        else:
            self.additional_dirs = None

    def scan_url(self, url):
        print("---###[ SCANNING {0} ]###---".format(url))

        body = request.urlopen(url)
        page_enc = body.headers.get_content_charset() or 'UTF-8'

        try:
            for line in body:
                self.feed(line.decode(page_enc))
        except UnicodeDecodeError:
            pass

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

        if file_only_url not in self.checked_files and not file_only_url.endswith('/'):
            # Check for backups here
            print("Checking {0} for backups now:".format(file_only_url))
            self.check_url(file_only_url)

            if self.additional_dirs:
                self.check_dirs_for_backups(file_only_url)

            self.checked_files.append(file_only_url)

        if url_to_spider not in self.spidered_links:
            # Begin spidering a new page
            self.spidered_links.append(url_to_spider)

            self.root = url_to_spider[:url_to_spider.rfind("/") + 1]
            self.scan_url(url_to_spider)

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