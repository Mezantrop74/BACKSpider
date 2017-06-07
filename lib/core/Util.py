#!/usr/bin/env python3
import sys


class Util:
    @staticmethod
    def read_file_into_array(file_path):
        try:
            with open(file_path) as file:
                file_lines = []
                for dir_line in file:
                    file_lines.append(dir_line.rstrip())

                return file_lines

        except FileNotFoundError:
            print("[ERROR] Could not find the file you specified. ({0})".format(dir_list))
            sys.exit(1)