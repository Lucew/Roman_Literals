from RomanLiterals.Converter import make_complete_literals_dict, number2literal, to_literal, from_literal
from RomanLiterals.JsConverter import get_literals_js_function
from RomanLiterals.SortingDict import SortingDict
import time
from termcolor import colored
from tqdm import tqdm
import pytest


def test_invalid_numbers():
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

    # get the time
    timed = time.perf_counter() - timed

    # print the results
    print(f'{correct_guess}/{end_number-1} were translated correctly in {timed:0.4} s'
          f' ({correct_guess/(end_number-1)*100:0.2f} %).')

    # raise an error if not all numbers were detected correctly
    if correct_guess < end_number - 1:
        raise ValueError('Conversion from number to literal was not done correctly in every case!')


def test_several_literals(end_number=2999):

    # get the baseline function for the conversion
    conversion_function = get_literals_js_function()

    # check all the numbers
    correct_guess = 0
    timed = time.perf_counter()
    for number in tqdm(range(1, end_number), desc='Transforming numbers'):

        # get the correct literal
        literal = conversion_function(number)

        # translate the literal with our function
        estimated_number = from_literal(literal)

        correct_guess += int(estimated_number == number)

    # get the time
    timed = time.perf_counter() - timed

    # print the results
    print(f'{correct_guess}/{end_number - 1} were translated correctly in {timed:0.4} s'
          f' ({correct_guess / (end_number - 1) * 100:0.2f} %).')

    # raise an error if not all numbers were detected correctly
    if correct_guess < end_number - 1:
        raise ValueError('Conversion from literal to number was not done correctly in every case!')


def test_invalid_literals():
    with pytest.raises(ValueError, match="as the symbols are not in order!"):
        from_literal('MIIX')
    with pytest.raises(ValueError, match="can not subtract over tens digit border!"):
        from_literal('MIMIX')
    with pytest.raises(ValueError, match="input as this number can be simplified to"):
        from_literal('MDM')
    with pytest.raises(ValueError, match="input as it contains symbols more than three times"):
        from_literal('MMMMM')


if __name__ == "__main__":
    test_several_user_inputs()
    test_several_numbers(3000)
    test_invalid_numbers()
    test_several_literals(3000)
    test_invalid_literals()
