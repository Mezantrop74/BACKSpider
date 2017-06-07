#!/usr/bin/env python3
import sys
from urllib import parse
from multiprocessing import Pool
from lib.core import WebSpider


class DirScanner:
    def __init__(self, max_threads):
        self.threads = max_threads
        self.additional_dirs = []

    def scan(self, root_url, dir_list):
        print("Checking for additional directories to search...")
        try:
            with open(dir_list) as file:
                dir_urls = []
                for dir_line in file:
                    dir_urls.append(parse.urljoin(root_url, dir_line))

            thread_pool = Pool(int(self.threads))
            thread_pool.map(self.scan_dirs_threaded, dir_urls)

        except FileNotFoundError:
            print("[ERROR] Could not find the file you specified. ({0})".format(dir_list))
            sys.exit(1)

    def scan_dirs_threaded(self, url):
        if WebSpider.response_code(url) == 200:
            url = url.rstrip()
            if not url.endswith('/'):
                url += '/'

            if url not in self.additional_dirs:
                print("[200 - OK] Directory found: ", url)
                self.additional_dirs.append(url)