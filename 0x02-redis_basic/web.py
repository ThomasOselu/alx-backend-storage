#!/usr/bin/env python3
""" Optional Task 1 """

import requests
import redis
from functools import wraps
from typing import Any, Callable, Dict, List


def track_and_cache(method: Callable) -> Callable:
    """Tracks Access"""
    @wraps(method)
    def wrapper(url, *args, **kwargs):
        """Wrapper"""
        redis_instance = redis.Redis()
        key = f"count:{url}"
        cache = f"{url}"
        redis_instance.incr(key)
        cached = redis_instance.get(cache)
        if cached is not None:
            return cached.decode('utf-8')
        response = method(url, *args, **kwargs)
        redis_instance.setex(cache, 10, response)
        return response
    return wrapper


@track_and_cache
def get_page(url: str) -> str:
    """uses the requests module
    to obtain the HTML content of a particular URL
    and returns it"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    """Main function"""
    get_page("http://slowwly.robertomurray.co.uk")
