#!/usr/bin/env python3
from urllib import parse
from multiprocessing import Pool
from lib.core import Util


class DirScanner:
    def __init__(self, max_threads):
        self.threads = max_threads
        self.additional_dirs = []

    def scan(self, root_url, dir_list):
        print("Checking for additional directories to search...")
        dir_urls = []
        dir_lines = Util.read_file_into_array(dir_list)

        for dir_line in dir_lines:
            dir_urls.append(parse.urljoin(root_url, dir_line))

        thread_pool = Pool(int(self.threads))
        thread_pool.map(self.scan_dirs_threaded, dir_urls)

        print(len(self.additional_dirs))
        return self.additional_dirs

    def scan_dirs_threaded(self, url):
        if Util.is_200_response(url):
            url = url.rstrip()
            if not url.endswith('/'):
                url += '/'

            # TODO: This isn't appending to additional_dirs
            if url not in self.additional_dirs:
                print("[200 - OK] Directory found: ", url)
                self.additional_dirs.append(url)
