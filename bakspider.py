#!/usr/bin/env python3
import sys
import argparse
import logging
from lib.core import SiteScanner
from lib.core import DirScanner
from lib.utils import Output
from lib.utils.WebUtils import WebUtils
import lib.utils.FileUtils as FileUtils


if sys.version_info < (3, 0):
    print("[ERROR] BAKSpider requires Python 3.0 or above")
    sys.exit(1)


# TODO: Catch keyboardinterrupt
def parse_args():
    parser = argparse.ArgumentParser(
        description="Attempts to find old files such as un-removed backups/configs on the web "
                    "server by either crawling the website or using dictionary based attacks.",
        epilog="Please report any issues on the GitHub repo."
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument("-u", "--url", help="The Target URL (e.g. http://www.example.com/)", required=True)

    parser.add_argument("-d", "--dir",
                        help="File containing additional directories to check for backups, "
                        "this option can increase scan time dramatically.",
                        required=False)

    parser.add_argument("-b", "--bakext", default="dic/common-extensions.txt", required=False,
                        help="File containing backup extensions to search for. (Default: dic/common-extensions.txt)")

    parser.add_argument("-e", "--ext", default="dic/whitelist-extensions.txt", required=False,
                        help="Whitelist extensions, only URLs with this extension will be checked for backups.")

    parser.add_argument("-t", help="Maximum number of concurrent threads (Default: 8)",
                        metavar="THREAD_COUNT", dest="threads", default=8, required=False)

    parser.add_argument("--debug", help="Enables verbose output, useful for debugging.",
                        action="store_true", required=False)

    output = Output()
    output.show_header(1)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)


def process(args):
    output = Output()
    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
    logger = logging.getLogger("bakspider")

    if args.debug:
        logger.info('Debug mode is enabled, output will be verbose.')
    else:
        logger.disabled = True

    if not WebUtils.is_valid_target_url(args.url):
        output.error("The URL you specified is not in the correct format, see examples:")
        print("\nValid examples:")
        output.status("http://www.example.com/")
        output.status("http://example.com/")
        print("\nInvalid examples:")
        output.negative("www.example.com")
        output.negative("http://www.example.com")
        sys.exit(1)


    # Check host is online
    if WebUtils.is_200_response(args.url):
        output.page_found("{0} -> Beginning scan...".format(args.url), False)
    else:
        output.error("The URL you specified is returning an invalid response code.")
        sys.exit(1)

    website = SiteScanner(args.url, output, args.threads)

    if args.dir:
        dir_scan = DirScanner(args.url, args.dir, output)
        website.additional_dirs = dir_scan.scan(args.threads)

    website.backup_extensions = FileUtils.read_file_into_array(args.bakext)
    website.whitelist_extensions = FileUtils.read_file_into_array(args.ext)
    website.begin_scan()

# TODO: Check if we are flooding the host and adjust a timeout to slow down requests
if __name__ == "__main__":
    parse_args()
