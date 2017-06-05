import os
import sys
import argparse
from urllib import request
from urllib import error
from urllib import parse
from urllib.parse import urlsplit
from urllib.parse import urlparse
from html.parser import HTMLParser

spidered_links = []
checked_files = []
additional_dirs = []
backup_extensions = ["backup", "bck", "old", "save", "bak", "sav", "~",
                     "copy", "old", "orig", "tmp", "txt", "back"]
skipped_extensions = ["pdf"]


class WebPage(HTMLParser):
    """Class to help with our webpage operations."""
    def __init__(self, url, root):
        HTMLParser.__init__(self)
        self.url = url
        self.root = root
        return

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.parse_href(value)
        return

    def parse_href(self, link):
        #print("href found:", link)

        # TODO: Maybe consolidate these if-statements, will have to calculate performance.
        if "://" in link:  # Check if relative or absolute
            if link.startswith("{0.scheme}://{0.netloc}/".format(urlsplit(self.root))):
                self.parse_url(link)
        else:
            url = parse.urljoin(self.root, link)
            self.parse_url(url)

        return

    def parse_url(self, url):

        parsed_url = urlparse(url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

        #print("Parsed URL:", url, "Clean URL:", clean_url)

        self.spider_url(url, clean_url);

        return

    def spider_url(self, url_to_spider, file_only_url):

        if not self.is_valid_url(file_only_url):
            return

        if file_only_url not in checked_files and not file_only_url.endswith('/'):
            # Check for backups here
            print("Checking {0} for backups now::".format(file_only_url))
            self.scan_for_backups(file_only_url)
            checked_files.append(file_only_url)

        if url_to_spider not in spidered_links:
            root = url_to_spider[:url_to_spider.rfind("/") + 1]
            #print("Root is:", root)

            spidered_links.append(url_to_spider)

            #input("Please ENTER to continue...")

            WebPage(url_to_spider, root).scan()
        return

    def is_valid_url(self, url):
        if url.startswith("mailto"):
            return 0

        return 1

    # TODO: Check for certain extensions (exclude PDF etc.)
    # TODO: Move core login into a seperate method.
    def scan_for_backups(self, url):
        self.check_url(url)

        filename = os.path.basename(url)
        print("Checking dirs for", filename)

        for dir_name in additional_dirs:
            dir_url = parse.urljoin(dir_name, filename)
            self.check_url(dir_url)

        input("Continue?...")

        return

    def check_url(self, url):
        # Check with original extension
        for ext in backup_extensions:
            bak_url = "{0}.{1}".format(url, ext)
            print(bak_url)

            if self.response_code(bak_url) == 200:
                print("[200 - OK] Backup found: {0}".format(bak_url))

        # Check without original extension
        url = url.rsplit('.', 1)[0]
        for ext in backup_extensions:
            bak_url = "{0}.{1}".format(url, ext)
            print(bak_url)

            if self.response_code(bak_url) == 200:
                print("[200 - OK] Backup found: {0}".format(bak_url))
        return

    def scan(self):
        print("---###[ SCANNING {0} ]###---".format(self.url))

        body = request.urlopen(self.url)
        page_enc = body.headers.get_content_charset() or 'UTF-8'

        try:
            for line in body:
                self.feed(line.decode(page_enc))
        except UnicodeDecodeError:
            pass

        return

    def is_accessible(self):
        return self.response_code(self.url) == 200

    #def response_code(self):
    #    try:
    #        return request.urlopen(self.url).getcode()
    #    except error.URLError as e:
    #        print("An exception occurred, does the domain exist? [{0}]".format(self.url))
    #        print(repr(e))
    #        sys.exit(1)

    # TODO: Check for redirect to 404 page (will return 200)
    # TODO: Allow custom timeout
    @staticmethod
    def response_code(url):
        try:
            return request.urlopen(url).getcode()
        except Exception as e:
            print (e)
            return 404


# TODO: Catch FileNotFoundError
def scan_dirs(root, dir_list):
    print("Checking for additional directories to search...")
    with open(dir_list) as file:
        for dir_line in file:
            url = parse.urljoin(root, dir_line)
            if WebPage.response_code(url) == 200:
                url = url.rstrip()
                if not url.endswith('/'):
                    url += '/'

                print("[200 - OK] Directory found: ", url)
                additional_dirs.append(url)
    return


def parse_args():
    parser = argparse.ArgumentParser(
        description="Attempts to find old files such as un-removed backups/configs on the web "
                    "server by either crawling the website or using dictionary based attacks.",
        epilog="Please report any issues to: matt@m-croston.co.uk"
    )

    parser.add_argument("-u", "--url", help="The Target URL (e.g. http://www.example.com/)", required=True)
    parser.add_argument("-d", "--dir", help="File containing additional directories to check for backups, "
                                            "this option can increase scan time dramatically.", required=False)

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    process(args)
    return


# TODO: Check the URL is in the correct format http://www.example.com/
def process(args):
    root = WebPage(args.url, args.url)

    if root.is_accessible():
        print("{0} [200 - OK] :: Beginning scan...".format(args.url))
        # TODO: Check the dir argument has been passed.
        scan_dirs(args.url, args.dir)
        input("Continue?...")
        root.scan()
    else:
        print("The URL you specified is returning an invalid response code.")
        sys.exit(1)
    return


if __name__ == "__main__":
    parse_args()
