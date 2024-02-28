import functools
import requests

from collections import OrderedDict
from requests.exceptions import MissingSchema


def cache(max_limit=2):
    def internal(func):
        @functools.wraps(func)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))

            if cache_key in deco._cache:
                deco._cache.move_to_end(cache_key, last=False)
                return deco._cache[cache_key]

            result = func(*args, **kwargs)

            if len(deco._cache) >= max_limit:
                deco._cache.popitem(last=False)
            deco._cache[cache_key] = result
            print(deco._cache)

            return result

        deco._cache = OrderedDict()

        return deco

    return internal


@cache()
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    try:
        res = requests.get(url)
        return res.content[:first_n] if first_n else res.content

    except MissingSchema:
        raise ValueError("PLEASE, ENTER VALID URL")
