#!/usr/bin/env python3
import sys
from lib.utils import Output


def read_file_into_array(file_path):
    try:
        with open(file_path) as file:
            file_lines = []
            for dir_line in file:
                if dir_line.strip() and not dir_line[0] == '#':
                    file_lines.append(dir_line.rstrip())

            return file_lines

    except FileNotFoundError:
        output = Output()
        output.error("Could not find the file you specified. ({0})".format(file_path))
        sys.exit(1)
