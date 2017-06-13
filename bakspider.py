#!/usr/bin/env python3
import sys
import argparse
from lib.core import Util
from lib.core import WebSpider
from lib.core import DirScanner

if sys.version_info < (3, 0):
    print("[ERROR] BAKSpider requires Python 3.0 or above")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Attempts to find old files such as un-removed backups/configs on the web "
                    "server by either crawling the website or using dictionary based attacks.",
        epilog="Please report any issues to: bugs@m-croston.co.uk"
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument("-u", "--url", help="The Target URL (e.g. http://www.example.com/)", required=True)

    parser.add_argument("-d", "--dir", help="File containing additional directories to check for backups, "
                        "this option can increase scan time dramatically.", required=False)

    parser.add_argument("-e", "--ext", help="File containing backup extensions to use. (Default: dic/common-ext.txt)",
                        default="dic/common-ext.txt", required=False)

    parser.add_argument("-t", help="Maximum number of concurrent threads (Default: 8)",
                        metavar="THREAD-COUNT", default=8, required=False)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)


# TODO: Check the URL is in the correct format http://www.example.com/
def process(args):
    if Util.is_200_response(args.url):
        print("{0} [200 - OK] :: Beginning scan...".format(args.url))

        if args.dir:
            dirscan = DirScanner(args.t)
            found_dirs = dirscan.scan(args.url, args.dir)

            for dir in found_dirs:
                print(dir)
                input("Cont?")

            root_page = WebSpider(args.url, args.url, args, found_dirs)
        else:
            root_page = WebSpider(args.url, args.url, args)

        root_page.scan()
    else:
        print("[ERROR] The URL you specified is returning an invalid response code.")
        sys.exit(1)


if __name__ == "__main__":
    parse_args()
