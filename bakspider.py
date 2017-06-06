#!/usr/bin/env python3
# TODO: Getting too large for one file, split into a full project.
import sys
import argparse
from urllib import parse
from multiprocessing import Pool

from lib.core import WebSpider

if sys.version_info < (3, 0):
    print("[ERROR] BAKSpider requires Python 3.0 or above")
    sys.exit(1)

# TODO: Reduce the scope of these if possible.
max_threads = 8

def scan_dirs(root, dir_list):
    print("Checking for additional directories to search...")
    try:
        with open(dir_list) as file:
            dir_urls = []
            for dir_line in file:
                dir_urls.append(parse.urljoin(root, dir_line))

        threadpool = Pool(int(max_threads))
        threadpool.map(scan_dirs_threaded, dir_urls)

    except FileNotFoundError:
        print("[ERROR] Could not find the file you specified. ({0})".format(dir_list))
        sys.exit(1)


def scan_dirs_threaded(url):
    if WebSpider.response_code(url) == 200:
        url = url.rstrip()
        if not url.endswith('/'):
            url += '/'

        if url not in additional_dirs:
            print("[200 - OK] Directory found: ", url)
            additional_dirs.append(url)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Attempts to find old files such as un-removed backups/configs on the web "
                    "server by either crawling the website or using dictionary based attacks.",
        epilog="Please report any issues to: matt@m-croston.co.uk"
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument("-u", "--url", help="The Target URL (e.g. http://www.example.com/)", required=True)

    parser.add_argument("-d", "--dir", help="File containing additional directories to check for backups, "
                        "this option can increase scan time dramatically.", required=False)

    parser.add_argument("-t", help="Maximum number of concurrent threads (Default: 8)",
                        metavar="THREAD-COUNT", default=8, required=False)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)


# TODO: Check the URL is in the correct format http://www.example.com/
def process(args):
    root = WebSpider(args.url, args.url)

    if root.is_accessible():
        print("{0} [200 - OK] :: Beginning scan...".format(args.url))
        global max_threads
        max_threads = args.t

        if args.dir:
            scan_dirs(args.url, args.dir)

        root.scan()
    else:
        print("[ERROR] The URL you specified is returning an invalid response code.")
        sys.exit(1)


if __name__ == "__main__":
    parse_args()
