#!/usr/bin/env python3
from urllib import request
from urllib.parse import urlparse
from os.path import splitext


# TODO: Check for redirect to 404 page (will return 200)
# TODO: Allow custom timeout
def is_200_response(url):
    try:
        return request.urlopen(url).getcode() == 200
    except Exception:
        return False


def is_valid_url(url):
    if url.startswith("http"):
        return True

    return False


def get_url_extension(url):
    path = urlparse(url).path
    ext = splitext(path)[1]

    return ext[1:].split(':')[0]