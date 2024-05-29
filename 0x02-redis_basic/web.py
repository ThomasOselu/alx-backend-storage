#!/usr/bin/env python3

"""
This module provides a CacheTracker class to track URL access counts and cache results with an expiration time of 10 seconds.
It also provides a get_page function to retrieve the HTML content of a URL, using the CacheTracker to cache the results.
"""

import time
import requests
from functools import wraps
from threading import Lock

class CacheTracker:
    """
    This class tracks URL access counts and caches results with an expiration time of 10 seconds.
    """
    _cache = {}
    _lock = Lock()

    @classmethod
    def _get_cache_key(cls, url):
        """
        Returns the cache key for the given URL.
        """
        return f"count:{url}"

    @classmethod
    def _get_cache_value(cls, url):
        """
        Returns the cache value for the given URL.
        """
        cache_key = cls._get_cache_key(url)
        with cls._lock:
            if cache_key in cls._cache:
                return cls._cache[cache_key]
            else:
                return None

    @classmethod
    def _set_cache_value(cls, url, value):
        """
        Sets the cache value for the given URL.
        """
        cache_key = cls._get_cache_key(url)
        with cls._lock:
            cls._cache[cache_key] = value

    @classmethod
    def increment_access_count(cls, url):
        """
        Increments the access count for the given URL.
        """
        cache_value = cls._get_cache_value(url)
        if cache_value:
            cache_value['count'] += 1
            cache_value['last_accessed'] = time.time()
        else:
            cache_value = {'count': 1, 'last_accessed': time.time(), 'content': None}
            cls._set_cache_value(url, cache_value)

    @classmethod
    def get_cached_content(cls, url):
        """
        Returns the cached content for the given URL if it exists and is not expired.
        """
        cache_value = cls._get_cache_value(url)
        if cache_value and time.time() - cache_value['last_accessed'] < 10:
            return cache_value['content']
        return None

    @classmethod
    def cache_content(cls, url, content):
        """
        Caches the content for the given URL.
        """
        cache_value = cls._get_cache_value(url)
        if cache_value:
            cache_value['content'] = content
            cache_value['last_accessed'] = time.time()
        else:
            cls._set_cache_value(url, {'count': 1, 'last_accessed': time.time(), 'content': content})


def cached(func):
    """
    A decorator to cache the results of a function.
    """
    @wraps(func)
    def wrapper(url):
        CacheTracker.increment_access_count(url)
        cached_content = CacheTracker.get_cached_content(url)
        if cached_content:
            return cached_content
        content = func(url)
        CacheTracker.cache_content(url, content)
        return content
    return wrapper


@cached
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL, using the CacheTracker to cache the results.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    return response.text
