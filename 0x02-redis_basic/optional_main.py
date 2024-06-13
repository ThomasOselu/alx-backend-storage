#!/usr/bin/env python3
"""
Optional Main file
"""
from time import sleep
from redis import Redis

get_page = __import__('web').get_page

redis = Redis()


url = "http://slowwly.robertomurray.co.uk"
print(get_page(url))
print("---------------------------")
print(get_page(url))

sleep(10)

print(get_page(url))
