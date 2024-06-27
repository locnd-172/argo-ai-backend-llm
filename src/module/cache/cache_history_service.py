from typing import Dict, List
from collections import OrderedDict


class LimitedSizeDict(OrderedDict):
    def __init__(self, max_size=3, *args, **kwargs):
        self.max_size = max_size
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if len(self) >= self.max_size:
            self.popitem(last=False)
        super().__setitem__(key, value)


# In-memory cache to store the history
cache = LimitedSizeDict(max_size=3)


def write_cache(session_id: str, sender_data: str, response: str):
    """
    Write the cache data for a given session_id to the in-memory cache dictionary.
    Enforces a maximum of three session_ids and a maximum of five cache entries per session_id.
    """
    global cache
    current_cache_data = {"user": sender_data, "bot": response}
    if session_id not in cache:
        cache[session_id] = [current_cache_data]
    else:
        # add cache per session_id
        current_cache: list = cache[session_id]
        current_cache = current_cache[-2:]
        current_cache.append(current_cache_data)
        # add session_id
        cache[session_id] = current_cache


def read_cache_by_session_id(session_id: str) -> List[Dict[str, str]]:
    """
    Read the cache data for a given session_id from the in-memory cache dictionary.
    Returns an empty list if the session_id is not found.
    """
    try:
        current_cache = cache.get(session_id, [])
        return current_cache
    except Exception as e:
        return []
