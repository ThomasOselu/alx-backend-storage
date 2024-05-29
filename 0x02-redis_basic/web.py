#!/usr/bin/env python3
"""
Caching request module
"""
import time
from functools import wraps
import requests

class CacheTracker:
    CACHE = {}

    @staticmethod
    def get_page_from_cache(url):
        if url in CacheTracker.CACHE and time.time() - CacheTracker.CACHE[url]['time'] < 10:
            return CacheTracker.CACHE[url]['content']
        return None

    @staticmethod
    def track_url_access(url):
        if url in CacheTracker.CACHE:
            CacheTracker.CACHE[url]['count'] += 1
        else:
            CacheTracker.CACHE[url] = {'count': 1, 'time': time.time(), 'content': None}

def cache_tracker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        content = CacheTracker.get_page_from_cache(url)
        if content is not None:
            CacheTracker.track_url_access(url)
            return content
        content = func(*args, **kwargs)
        CacheTracker.CACHE[url] = {'content': content, 'time': time.time()}
        CacheTracker.track_url_access(url)
        return content
    return wrapper

@cache_tracker
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
