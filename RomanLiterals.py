from termcolor import colored
from collections import OrderedDict
import js2py
from tqdm import tqdm


# literature collection
"""
Idea from:
https://cs6-gitlab.cs6.fau.de/lehre/swat/ss2020/dojo1/-/blob/master/Coding-Dojo-Roman.pdf

Roman number explanation from:
http://www.web40571.clarahost.co.uk/roman/1999.htm

# Additional rules from
http://www.novaroma.org/via_romana/numbers.html
"""


# a helper function to separate all digits from int
def int2digits(input_number: int):
    string_representation = str(input_number)
    digits_number = len(string_representation)
    return [int(digit)*10**(digits_number-counter-1) for counter, digit in enumerate(string_representation)]


# a function to make the complete literals dict
def make_complete_literals_dict(valid_literals: dict):
    # create an empty dict, where we will store all numbers and literals including "second level" literals
    # like IX, IL
    # also already put in known literals, so we can ignore ambiguities like V=VX
    complete_literals_dict = valid_literals.copy()

    # extend the dict by all possible subtraction numbers
    for number, literal in valid_literals.items():
        for lower_number, lower_literal in valid_literals.items():
            if number == lower_number:
                break
            second_level_number = number - lower_number
            second_level_literal = lower_literal + literal

            # put it into the complete literals dict but check whether is already in there
            if second_level_number not in complete_literals_dict:
                complete_literals_dict[second_level_number] = second_level_literal

    # order the dict
    complete_literals_dict = OrderedDict([*sorted(complete_literals_dict.items())])

    return complete_literals_dict


# a function to convert a tens digit to the corresponding literal
def tens_digit_to_literal(tens_digit: int, complete_literals_dict: dict):

    # save the number
    tmp_digit = tens_digit

    # translate the number
    tens_digit_literal = ''
    for number, literal in list(complete_literals_dict.items())[::-1]:

        # break when remainder is zero
        if tens_digit == 0:
            break

        # check whether the descending literal fits more than zero times (is part of the complete literal)
        quotient, temp_remainder = divmod(tens_digit, number)

        if quotient > 3:
            raise ValueError(f'Something went wrong with the conversion of input [{tens_digit}].')
        elif quotient > 0:
            tens_digit_literal += quotient * literal
            tens_digit = temp_remainder

    return tens_digit_literal


def number2literal(input_number: int, complete_literals: dict):

    # get the tens digits
    tens_digits = int2digits(input_number)

    # make the empty literal
    complete_literal = ''

    # iterate over every tens digit
    for tens_digit in tens_digits:
        complete_literal += tens_digit_to_literal(tens_digit, complete_literals)

    return complete_literal


def recreate_js_function(file_path='StolenConverter.js'):

    # get the javascript functions
    functions = js2py.run_file(file_path)[1]

    def interesting_function(input_number: int):
        return functions.toRoman(str(input_number))

    return interesting_function


def main():
    # a list for the test cases
    test_cases = {1: 'I', 10: 'X', 7: 'VII', 1999: 'MCMXCIX', 2989: 'MMCMLXXXIX', 2999: 'MMCMXCIX'}

    # a dict of valid literals
    valid_literals = OrderedDict({1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'})

    # make the complete literals dict
    complete_literals_dict = make_complete_literals_dict(valid_literals)

    # iterate through all test cases
    for number, literal in test_cases.items():
        res = number2literal(number, complete_literals_dict)
        print(colored(f'{"+" if res == literal else "-"} | For {number=} the result is {res}'
                      f' and it is {"" if res == literal else "not "} correct '
                      f'(expected = {literal}).', "green" if res == literal else "red"))


def test_mutliple_cases(end_number=2999):

    # get the baseline function
    conversion_function = recreate_js_function()

    # a dict of valid literals
    valid_literals = OrderedDict({1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'})

    # make the complete literals dict
    complete_literals_dict = make_complete_literals_dict(valid_literals)

    # check all the numbers
    correct_guess = 0
    for number in tqdm(range(1, end_number), desc='Transforming numbers'):
        estimation = number2literal(number, complete_literals_dict)
        groundtruth = conversion_function(number)
        correct_guess += int(estimation == groundtruth)

    # print the results
    print(f'{correct_guess}/{end_number-1} were translated correctly ({correct_guess/(end_number-1):0.2f}).')


if __name__ == '__main__':
    # main()
    test_mutliple_cases(1500)