import redis
import pickle


redis_instance_counter = 0


class RedisCache:
    def __init__(self):
        global redis_instance_counter
        self.redis = redis.Redis(host='localhost', port=6380, db=redis_instance_counter)
        redis_instance_counter += 1
        self.length = 0

    def __setitem__(self, key, value):
        kew_is_new = key not in self
        self.redis.set(pickle.dumps(key), pickle.dumps(value))
        # Update it after setting the key to not increase the counter without being sure the value is possible to set.
        if kew_is_new:
            self.length += 1

    def __getitem__(self, key):
        value = self.redis.get(pickle.dumps(key))
        if value is None:
            raise KeyError()
        return pickle.loads(value)

    def __delitem__(self, key):
        self.redis.delete(pickle.dumps(key))
        if key in self:
            self.length -= 1

    def __contains__(self, item):
        return self.redis.get(pickle.dumps(item)) is not None

    def __len__(self):
        return self.length
