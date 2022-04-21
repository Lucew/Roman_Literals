from RomanLiterals.Converter import make_complete_literals_dict, number2literal, to_literal
from RomanLiterals.JsConverter import get_literals_js_function
from RomanLiterals.SortingDict import SortingDict
import time
from termcolor import colored
from tqdm import tqdm
import pytest


def test_invalid_number():
    with pytest.raises(ValueError, match="invalid literal for "):
        to_literal(-1)
    with pytest.raises(ValueError, match="Something went wrong with the conversion of input"):
        to_literal(5000)


def test_several_user_inputs():
    # a list for the test cases
    test_cases = {1: 'I', 10: 'X', 7: 'VII', 1999: 'MCMXCIX', 2989: 'MMCMLXXXIX', 2999: 'MMCMXCIX'}

    # iterate through all test cases
    for number, literal in test_cases.items():
        res = to_literal(number)
        print(colored(f'{"+" if res == literal else "-"} | For {number=} the result is {res}'
                      f' and it is {"" if res == literal else "not "} correct '
                      f'(expected = {literal}).', "green" if res == literal else "red"))


def test_several_numbers(end_number=2999):

    # get the baseline function for the conversion
    conversion_function = get_literals_js_function()

    # a dict of valid literals
    valid_literals = SortingDict({1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'})

    # make the complete literals dict
    complete_literals_dict = make_complete_literals_dict(valid_literals)

    # check all the numbers
    correct_guess = 0
    timed = time.perf_counter()
    for number in tqdm(range(1, end_number), desc='Transforming numbers'):
        estimation = number2literal(number, complete_literals_dict)
        groundtruth = conversion_function(number)
        correct_guess += int(estimation == groundtruth)
    timed = time.perf_counter() - timed
    # print the results
    print(f'{correct_guess}/{end_number-1} were translated correctly in {timed:0.4} s'
          f' ({correct_guess/(end_number-1)*100:0.2f} %).')


if __name__ == "__main__":
    test_several_user_inputs()
    test_several_numbers(3000)
    test_invalid_number()
