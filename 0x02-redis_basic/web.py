#!/usr/bin/env python3
import requests
import redis
import functools


class Web:
    def __init__(self):
        """Initialize the Web class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def get_page(self, url: str) -> str:
        """Get the HTML content of a particular URL"""
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"
        if self._redis.exists(cache_key):
            return self._redis.get(cache_key).decode('utf-8')
        response = requests.get(url)
        self._redis.setex(cache_key, 10, response.text)
        self._redis.incr(count_key)
        return response.text

    def count_calls(self, method):
        """Count how many times a particular URL was accessed"""
        @functools.wraps(method)
        def wrapper(self, url: str):
            count_key = f"count:{url}"
            self._redis.incr(count_key)
            return method(self, url)
        return wrapper

    get_page = count_calls(get_page)

# Example usage:


web = Web()
print(web.get_page("http://slowwly.robertomurray.co.uk"))
print(web.get_page("http://slowwly.robertomurray.co.uk"))
print(web.get_page("http://slowwly.robertomurray.co.uk"))
