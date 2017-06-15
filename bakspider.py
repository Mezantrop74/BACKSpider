#!/usr/bin/env python3
import sys
import argparse
from lib.var import Config
from lib.core import Util
from lib.core import SiteScanner
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
                        metavar="THREAD_COUNT", dest="threads", default=8, required=False)

    parser.add_argument("--debug", help="Enables verbose output, useful for debugging.",
                        action="store_true", required=False)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)


# TODO: Check the URL is in the correct format http://www.example.com/
# TODO: Check required arguments are supplied
def process(args):
    if Util.is_200_response(args.url):
        print("{0} [200 - OK] :: Beginning scan...".format(args.url))

        if args.threads:
            Config.thread_count = int(args.threads)

        if args.debug:
            print("[DEBUG] Debug mode is enabled, output will be verbose.")
            Config.is_debug = True

        website = SiteScanner(args.url)

        if args.dir:
            website.additional_dirs = DirScanner.scan(args.url, args.dir, args.threads)

        website.backup_extensions = Util.read_file_into_array(args.ext)
        website.begin_scan()
    else:
        print("[ERROR] The URL you specified is returning an invalid response code.")
        sys.exit(1)


if __name__ == "__main__":
    parse_args()
