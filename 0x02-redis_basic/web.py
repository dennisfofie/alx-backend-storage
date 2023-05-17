#!/usr/bin/env python3
"""web scraping using requests module"""

import requests
from redis import Redis
import time
from functools import wraps


def text_decorator(method):
    """caching result through api calls"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        key = method.__qualname__ + "args"
        count = method.__qualname__ + "args"
        Redis().incr(key)
        result = Redis().get(count)
        if result:
            return str(result)

        time.sleep(10)
        return method(*args, **kwargs)

    return wrapper


@text_decorator
def get_page(url: str) -> str:
    "get information about a page"
    data = requests.get(url)
    return data.text
