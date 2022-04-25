import sys
import os
# check the python version first!
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    file_name = os.path.basename(__file__)[:-3]
    raise NotImplementedError(f'Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later is required to use {file_name}.')


class SortingDict(dict):
    """
    This class implements a self sorting ordered dict. After key insert it always updates its items according to a given
    function.
    """

    def __init__(self, initial_dictionary: dict, order_function=lambda t: t[0]):
        # initialize self
        super().__init__(initial_dictionary)

        # save the order function
        self.order_function = order_function

        # update the dict
        self._update()

    def _update(self):
        """
        This function updates the item order in the ordered dict according to the given function.
        """
        temp_dict = {key: self[key] for key in sorted(self)}
        self.clear()
        super().update(temp_dict)

    def __setitem__(self, key, val):

        # set the new value
        super().__setitem__(key, val)

        # update the dict
        self._update()

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            super().__setitem__(k, v)
            self._update()

    def copy(self):
        return SortingDict(self)


class AccessCounterDict(dict):

    def __init__(self, initial_dictionary: dict):
        super().__init__(initial_dictionary)

        # create an additional counter dict
        self.counter = dict.fromkeys(initial_dictionary.keys(), 0)
        self.max_key = ''

    def __getitem__(self, key):

        # get the value
        val = super().__getitem__(key)

        # increase the counter
        self._counter_increase(key)

        return val

    def _counter_increase(self, key):
        """
        We need this function in order to also keep track of the maximum counter while increasing.
        :param key: The keyword for the dictionary element we are accessing
        :return: None
        """

        # increase the counter
        self.counter[key] += 1

        # keep track of maximum counter
        if self.counter[key] > self.counter.get(self.max_key, -1):
            self.max_key = key

    def __setitem__(self, key, val):

        # set the new value
        super().__setitem__(key, val)

    def __repr__(self):

        # make the representation of this dict
        repr_str = '{' + \
                   ''.join([f'{repr(key)} [{repr(self.counter[key])}]: {repr(value)}, '
                            for key, value in super().items()]) + \
                   '}'
        return repr_str

    def get(self, key, value=None):
        res = super().get(key, value)
        if key in super().keys():
            self._counter_increase(key)
        return res

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            super().__setitem__(k, v)
            if k not in super().keys():
                self.counter[k] = 0

    def get_without_counter(self, key):
        return super().__getitem__(key)

    def get_access_counter(self, key):
        return self.counter[key]

    def max(self):
        return self. max_key, self.counter[self.max_key]