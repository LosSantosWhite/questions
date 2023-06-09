from functools import wraps
import time
from typing import Callable
import uuid

import redis
from redis import Redis

from app.config import config


class RedisClient:
    def __init__(self):
        self.conn = Redis.from_url(config.redis.dsn, max_connections=1)

    def acquire_lock(
        self,
        lock_name: str = "not_available",
        acquire_timeout: int = 3,
        lock_timeout: int = 3,
    ) -> bool:
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_timeout
        while time.time() < end:
            if self.setnx(lock_name, identifier):
                self.conn.expire(identifier, lock_timeout)
                return identifier
            elif not self.conn.ttl(lock_name):
                self.conn.expire(lock_name, lock_timeout)

        return False

    def setnx(self, lock_name: str, identifier: str):
        return self.conn.setnx(f"lock:{lock_name}", identifier)

    def realise_lock(
        self,
        identifier: str,
        lock_name: str = "not_available",
    ):
        pipe = self.conn.pipeline(True)
        lock_name = f"lock:{lock_name}"
        while True:
            try:
                pipe.watch(lock_name)

                if pipe.get(lock_name).decode() == identifier:
                    pipe.multi()

                    pipe.delete(lock_name)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError as err:
                return False
        return False

    def get(self, key: str):
        return self.conn.get(key)

    def append(self, key, *values):
        return self.conn.lpush(key, *values)

    def get_list(self, key: str):
        return self.conn.lrange(key, start=0, end=-1)


if __name__ == "__main__":
    r = RedisClient()
    print(r.conn.keys())
    print(r.get_list("questions_ids"))
    print(r.get_last_record())
