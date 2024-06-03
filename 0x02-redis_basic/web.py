#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import requests
import functools
import redis
from typing import Callable


def cache(ttl: int = 10) -> Callable:
    """
    A decorator to cache the result of a function for a certain amount of time.

    Args:
    ttl (int): The time to live in seconds. Defaults to 10.

    Returns:
    Callable: A decorator function.
    """

    cache = redis.Redis()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(url: str) -> str:
            """
            A wrapper function to cache the result of the decorated function.

            Args:
            url (str): The URL to get the page from.

            Returns:
            str: The HTML content of the page.
            """
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            if cache.exists(cache_key):
                return cache.get(cache_key).decode("utf-8")
            else:
                result = func(url)
                cache.setex(cache_key, ttl, result)
                cache.incr(count_key)
                return result
        return wrapper
    return decorator


@cache(ttl=10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a page.

    Args:
    url (str): The URL to get the page from.

    Returns:
    str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    print(get_page("http://google.com"))
    print(get_page("http://google.com"))
