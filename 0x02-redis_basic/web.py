#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import requests
import functools
import redis
from typing import Callable

def cache(ttl: int = 10):
    def decorator(func: Callable) -> Callable:
        cache = redis.Redis()
        @functools.wraps(func)
        def wrapper(url: str) -> str:
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
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    print(get_page("http://slowwly.robertomurray.co.uk"))
    print(get_page("http://slowwly.robertomurray.co.uk"))
