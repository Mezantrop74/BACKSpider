#!/usr/bin/env python3
from urllib import parse
from lib.utils.Output import Output
from lib.utils.WebUtils import WebUtils
import lib.utils.FileUtils as FileUtils
from multiprocessing.pool import ThreadPool


class DirScanner:
    def __init__(self, root_url, dir_list, output):
        self.root_url = root_url
        self.dir_list = dir_list
        self.output = output

    def scan(self, thread_count):
        self.output.progress("Checking for additional directories to search...")

        dir_urls = []
        dir_lines = FileUtils.read_file_into_array(self.dir_list)

        for dir_line in dir_lines:
            dir_urls.append(parse.urljoin(self.root_url, dir_line))

        thread_pool = ThreadPool(int(thread_count))
        found_dirs = thread_pool.map(DirScanner.scan_dirs_threaded, dir_urls)

        thread_pool.close()
        thread_pool.join()

        self.output.progress("Directory scan finished!")
        return [value for value in found_dirs if value is not None]

    @staticmethod
    def scan_dirs_threaded(url):
        if WebUtils.is_200_response(url):
            url = url.rstrip()
            if not url.endswith('/'):
                url += '/'

            output = Output()
            output.page_found("Directory found: {0}".format(url), True)
            return url
