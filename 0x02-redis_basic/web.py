#!/usr/bin/env python3
"""web scraping using requests module"""

import requests
from redis import Redis
from typing import Callable
import time
from functools import wraps


def text_decorator(expiration):
    """caching result through api calls"""

    def decorator(method: Callable) -> Callable:
        """first decorator"""

        @wraps(method)
        def wrapper(*args, **kwargs):
            """the wrapper function"""
            key = method.__qualname__ + "args"
            count = method.__qualname__ + "args"
            Redis().incr(key)
            result = Redis().get(count)
            if result:
                return str(result)
            results = method(*args, **kwargs)
            Redis().setex(key, expiration, results)
            return results

        return wrapper

    return decorator


@text_decorator(expiration=10)
def get_page(url: str) -> str:
    "get information about a page"
    data = requests.get(url)
    return data.text
