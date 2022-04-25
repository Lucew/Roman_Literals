from RomanLiterals.SortingDict import SortingDict
from math import log10
from RomanLiterals.SortingDict import AccessCounterDict

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

            # put it into the complete literals' dict but check whether is already in there
            if second_level_number not in complete_literals_dict:
                complete_literals_dict[second_level_number] = second_level_literal

    return complete_literals_dict


# a function to convert a tens' digit to the corresponding literal
def tens_digit_to_literal(tens_digit: int, complete_literals_dict: dict):

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


def to_literal(number: int):
    # a dict of valid literals
    valid_literals = SortingDict({1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'})

    # make the complete literals dict
    complete_literals_dict = make_complete_literals_dict(valid_literals)

    return number2literal(number, complete_literals_dict)


def from_literal(literal: str):

    # a dict of valid literals and their numbers
    valid_literals = AccessCounterDict({'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000})
    # reverse the dict to get valid numbers
    valid_numbers = {value: key for key, value in valid_literals.items()}

    # make all characters from the string upper case
    literal = literal.upper()

    # go through the string
    skip_literal = False
    result = 0
    last_value = 0
    for counter, char in enumerate(literal[::-1], start=1):

        # check whether we need to skip the current literals (because we already processed it with a subtraction
        if skip_literal:
            skip_literal = False  # next literal is interesting again
            continue
        else:

            # get the current value of the position
            current_value = valid_literals[char]

            # check whether its is smaller than the last added value (not allowed)
            # e.g. IIX is not allowed if we are at position -3 (first I). In this case I < 9 (IX) we processed right
            # before -> raise ValueError
            if current_value < last_value:
                raise ValueError(f'[{literal=}] is not a valid input as the symbols are not in order!')

            # go one step deeper and check whether we need to do subtraction
            # also we need to check to not run out of range when current value is the first character in the string
            if counter < len(literal):
                next_value = valid_literals.get_without_counter(literal[-counter-1])

                # check whether next value is smaller
                if next_value < current_value:

                    # check whether this subtraction is valid (only allowed to change each tens digit)
                    # meaning that IC is not allowed for example. Only one power of ten is allowed between them
                    if log10(current_value) - log10(next_value) > 1:
                        raise ValueError(f'[{literal=}]'
                                         f' is not a valid input as you can not subtract over tens digit border!')

                    # check whether this subtracted number makes sense
                    # for example DM for 500 makes no sense at it is shorter with just D
                    alternative_literal = valid_numbers.get(current_value - next_value)
                    if alternative_literal is not None:
                        raise ValueError(f'[{literal=}] is not a valid input as this number can be simplified to'
                                         f' {literal[:-counter-1] + alternative_literal}!')

                    # make the subtraction and raise the skip next flag
                    current_value = current_value - next_value
                    skip_literal = True

            # add the number to the result
            result += current_value

            # save the current added value to check for valid literals
            # e.g. IIX is not allowed
            last_value = current_value

    # check if we accessed the dict too often
    key, number = valid_literals.max()
    if number > 3:
        raise ValueError(f'[{literal=}] is not a valid input as it contains symbols more than three times'
                         f' ({number}x{key}).')

    return result


if __name__ == '__main__':
    # this code won't be tested since its is just demonstration (not necessary)
    print(to_literal(199))
    print(from_literal('MCMXCIX'))
    print(from_literal('MMC'))
