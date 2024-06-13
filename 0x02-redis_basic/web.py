#!/usr/bin/env python3
""" Optional Task 1 """

import requests
import redis
from functools import wraps
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_result(expiration=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url, *args, **kwargs):
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            redis_client.incr(count_key)

            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url, *args, **kwargs)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


@cache_result(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"

    print("Fetching the page...")
    page_content = get_page(test_url)
    print(page_content[:500])

    time.sleep(5)
    print("Fetching the page again (should hit the cache)...")
    page_content = get_page(test_url)
    print(page_content[:500])

    time.sleep(10)
    print("Fetching the page after cache expiration...")
    page_content = get_page(test_url)
    print(page_content[:500])
