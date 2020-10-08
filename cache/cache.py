import functools
from .function_parameters import FunctionArguments
from collections import deque


class Cache:
    def __init__(self):
        # si le meto un redis, meterle un ID o algo a las keys antes con f-strings para evitar overlap con otras instancias.
        self.cached = {}

    def __len__(self):
        return len(self.cached)

    def __setitem__(self, key, value):
        self.cached[key] = value

    def __getitem__(self, key):
        return self.cached[key]

    def __contains__(self, item):
        return item in self.cached


class FunctionCallCache(Cache):
    """ Decorator to save function results. """

    def __init__(self, decorated_function):
        super().__init__()
        self.decorated_function = decorated_function

    def __call__(self, *args, **kwargs):
        function_arguments = FunctionArguments(*args, **kwargs)
        print(f'{self.decorated_function} is being called with the following arguments: {function_arguments}')
        # Look up in the cache
        try:
            result = self[function_arguments]
        except KeyError:
            # Result was not found. Calculate it as usual (just calling the decorated function) and save the result
            # in the cache for future calls
            result = self.decorated_function(*args, **kwargs)
            self[function_arguments] = result
            print('Result added to the cache.')
        else:
            print('Result found on cache!')
        return result


class FunctionCallSizeLimitedCache(FunctionCallCache):
    """ Decorator to save function results with a limited memory usage. """

    def __init__(self, decorated_function, max_size=2):
        super().__init__(decorated_function)
        self.access_sorted_items = deque(maxlen=max_size)

    @property
    def max_size_reached(self):
        return len(self.access_sorted_items) == self.access_sorted_items.maxlen

    def remove_unused_item(self):
        """ Removes the item accessed used the longest time ago. This method removes the item both from the item list
            and the internal cache. """
        item_to_remove = self.access_sorted_items.popleft()
        del self.cached[item_to_remove]

    def __setitem__(self, key, value):
        """ Checks the cache limit and makes space if necessary. """
        if key in self.access_sorted_items:  # to avoid duplicates and move the item to the top of the deque after readding it.
            self.access_sorted_items.remove(key)
            del self.cached[key]
        elif self.max_size_reached:
            self.remove_unused_item()
        self.access_sorted_items.append(key)
        super().__setitem__(key, value)
