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

