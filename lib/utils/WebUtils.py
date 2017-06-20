#!/usr/bin/env python3
from urllib import request


# TODO: Check for redirect to 404 page (will return 200)
# TODO: Allow custom timeout
def is_200_response(url):
    try:
        return request.urlopen(url).getcode() == 200
    except Exception:
        return False


def is_valid_url(url):
    if url.startswith("mailto"):
        return False

    return True
