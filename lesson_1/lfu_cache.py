import functools
import requests

from collections import OrderedDict
from requests.exceptions import MissingSchema


def cache(max_limit=2):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))

            if cache_key in deco._cache:
                deco._access_count[cache_key] += 1
                deco._cache.move_to_end(cache_key, last=True)
                return deco._cache[cache_key]

            result = f(*args, **kwargs)

            if len(deco._cache) >= max_limit:
                lfu_url = min(deco._access_count, key=deco._access_count.get)
                deco._cache.pop(lfu_url)
                deco._access_count.pop(lfu_url)

            deco._cache[cache_key] = result
            deco._access_count[cache_key] = 1
            return result

        deco._cache = OrderedDict()
        deco._access_count = {}

        return deco
    return internal


@cache()
def fetch_url(url: str, first_n: int = 100):
    """Fetch a given url"""
    try:
        res = requests.get(url)
        return res.content[:first_n] if first_n else res.content

    except MissingSchema:
        raise ValueError("PLEASE, ENTER VALID URL")
