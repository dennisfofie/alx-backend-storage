#!/usr/bin/env python3
"""Redis project using redis python client"""
from functools import wraps
import redis
import uuid
from typing import Union, Optional, Callable


def replay(method):
    """display the history of calls"""
    input_ = method.__qualname__ + ":inputs"
    output_ = method.__qualname__ + ":outputs"

    input_o = redis.Redis.lrange(
        input_,
        0,
    )
    output_o = redis.Redis.lrange(output_, 0, -1)

    print(f"{method.__qualname__} was called {len(input_)} times:")

    for args, output in zip(input_o, output_o):
        args = eval(args.decode())
        print(f"{method.__qualname__}(*{args}) -> {output.decode()}")


def call_history(method: Callable) -> Callable:
    """adding inputs and outputs"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """add to the redis using rpush"""
        input_ = method.__qualname__ + ":inputs"
        output_ = method.__qualname__ + ":outputs"
        self._redis.rpush(input_, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_, output)
        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """count redis instances decorators"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper func to maintain the doctring"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """redis client using redis.py"""

    def __init__(self):
        """initialize the redis instance as a private"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """storing data in redis database"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> any:
        """Changing the format of the data type"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Convert the output to string"""
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """convert the output to string"""
        return self.get(key, fn=int)
