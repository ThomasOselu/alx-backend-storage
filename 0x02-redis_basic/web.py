#!/usr/bin/env python3
"""
Caching request module
"""
import requests
import time
from functools import wraps


CACHE_EXPIRATION = 10  # in seconds
url_access_counts = {}


def cache_with_expiry(expiration):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(url):
            # Check if the result is cached and not expired
            if url in cache and time.time() - cache[url]['timestamp'] < expiration:
                return cache[url]['content']

            # If not cached or expired, fetch the content
            content = func(url)
            # Update cache
            cache[url] = {'content': content, 'timestamp': time.time()}
            return content

        return wrapper

    return decorator


def track_url_access(func):
    @wraps(func)
    def wrapper(url):
        if url in url_access_counts:
            url_access_counts[url] += 1
        else:
            url_access_counts[url] = 1
        return func(url)

    return wrapper


@cache_with_expiry(CACHE_EXPIRATION)
@track_url_access
def get_page(url):
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Testing the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))  # This will take some time to execute due to the simulated delay
    print(f"Access count for {url}: {url_access_counts[url]}")

    # Testing caching behavior
    print(get_page(url))  # This should return immediately from cache
    time.sleep(5)  # Sleep for less than the expiration time
    print(get_page(url))  # This should return immediately from cache again

    # Wait for cache to expire
    time.sleep(CACHE_EXPIRATION)
    print(get_page(url))  # This should fetch the page again due to cache expiration
