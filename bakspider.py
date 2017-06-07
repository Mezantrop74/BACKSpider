#!/usr/bin/env python3
import sys
import argparse
from lib.core import WebSpider
from lib.core import DirScanner

if sys.version_info < (3, 0):
    print("[ERROR] BAKSpider requires Python 3.0 or above")
    sys.exit(1)

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

    parser.add_argument("-e", "--ext", help="File containing backup extensions to use. (Default: dic/bak-ext.txt)",
                        default="dic/bak-ext.txt", required=False)

    parser.add_argument("-t", help="Maximum number of concurrent threads (Default: 8)",
                        metavar="THREAD-COUNT", default=8, required=False)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)


# TODO: Check the URL is in the correct format http://www.example.com/
def process(args):
    root = WebSpider(args.url, args.url, args)

    if root.is_accessible():
        print("{0} [200 - OK] :: Beginning scan...".format(args.url))

        if args.dir:
            dirscan = DirScanner(args.t)
            dirscan.scan(args.url, args.dir)

        root.scan()
    else:
        print("[ERROR] The URL you specified is returning an invalid response code.")
        sys.exit(1)


if __name__ == "__main__":
    parse_args()
