#!/usr/bin/env python3
import sys
from urllib import request


class Util:
    @staticmethod
    def read_file_into_array(file_path):
        try:
            with open(file_path) as file:
                file_lines = []
                for dir_line in file:
                    if dir_line.strip() and not dir_line[0] == '#':
                        file_lines.append(dir_line.rstrip())

                return file_lines

        except FileNotFoundError:
            print("[ERROR] Could not find the file you specified. ({0})".format(file_path))
            sys.exit(1)

    # TODO: Check for redirect to 404 page (will return 200)
    # TODO: Allow custom timeout
    @staticmethod
    def is_200_response(url):
        try:
            return request.urlopen(url).getcode() == 200
        except Exception:
            return False

    @staticmethod
    def is_valid_url(url):
        if url.startswith("mailto"):
            return False

        return True
