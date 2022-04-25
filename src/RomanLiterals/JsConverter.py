import json
import js2py
from tqdm import tqdm
import os


def recreate_js_function(file_path=None, to_roman=True):

    # create file path
    if file_path is None:
        file_path = os.path.join(os.path.split(__file__)[0], 'StolenConverter.js')

    # get the javascript functions
    functions = js2py.run_file(file_path)[1]

    if to_roman:
        def interesting_function(input_number: int):
            return functions.toRoman(str(input_number))
    else:
        def interesting_function(input_number: int):
            return functions.fromRoman(str(input_number))

    return interesting_function


def make_literal_dict(file_path=None):

    # create file path
    if file_path is None:
        file_path = os.path.join(os.path.split(__file__)[0], 'literals.json')

    # get the json function
    conversion_function = recreate_js_function()

    # make dict
    literals_dict = {key: "" for key in range(1, 3000)}

    # create all the literals
    for number in tqdm(range(1, 3000), desc='Creating the literals with js'):
        literal = conversion_function(number)
        literals_dict[number] = literal

    with open(file_path, 'w') as f:
        f.write(json.dumps(literals_dict))


def get_literal_dict(file_path=None, fresh=False):

    # create file path
    if file_path is None:
        file_path = os.path.join(os.path.split(__file__)[0], 'literals.json')

    # create new json if fresh is wished
    if fresh or not os.path.isfile(file_path):
        make_literal_dict(file_path)

    # load the dict and return it
    with open(file_path, 'r') as f:
        literals_dict = json.load(f)

    # change the keys to numbers
    literals_dict = {int(k): v for k, v in literals_dict.items()}

    return literals_dict


def get_literals_js_function():

    # get the dict
    literals_dict = get_literal_dict()

    def temp_fnc(number: int):

        # get the literals from the dict
        literal = literals_dict.get(number)

        # raise ValueError if not found
        if literal is None:
            raise ValueError('Literal could not be created by JS function.')

        return literal

    return temp_fnc


def get_number_js_function():

    # get the dict
    literals_dict = get_literal_dict()

    # reverse the dict
    numbers_dict = {value: key for key, value in literals_dict.items()}

    def temp_fnc(literal: str):

        # get the literals from the dict
        number = numbers_dict.get(literal)

        # raise ValueError if not found
        if number is None:
            raise ValueError('Number could not be created by JS function.')

        return number

    return temp_fnc



if __name__ == '__main__':
    print(get_literal_dict())
    print(get_number_js_function()('MMI'))
