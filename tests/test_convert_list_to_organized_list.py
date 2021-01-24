import pytest

from convert_list_to_organized_list import ConvertListToOrganizedList
from metadata import MetaData
from string_to_list_converter import StringToListConverter
from string_validator import StringValidator
from operators import *

OPERATORS_DICTIONARY = {
    '+': Plus(),
    '-': Minus(),
    '*': Multiplication(),
    '/': Division(),
    '^': Power(),
    '~': Negation(),
    '%': Modulo(),
    '!': Factorial(),
    '@': Average(),
    '$': Maximum(),
    '&': Minimum()
}

TEST_DATA = [
    ("5+7*9!", [5, '+', 7, '*', 9, '!', 0]),
    ("4+4", [4, '+', 4]),
    ("--4", [0, '-', '(', 0, '-', 4, ')']),
    ("4--(-5$7)",
     [4, '-', '(', 0, '-', '(', 0, '-', 5, '$', 7, ')', ')']),
    ("---2&1",
     [0, '-', '(', 0, '-', '(', 0, '-', 2, '&', 1, ')', ')']),
    ("-~-4+1*-3!",
     [0, '-', '(', 0, '~', '(', 0, '-', 4, ')', ')', '+', 1, '*',
      '(', 0, '-', 3, '!', 0, ')']),

]


@pytest.mark.parametrize("equation,expected", TEST_DATA)
def test_create_organize_list_convertor(equation, expected):
    # Set up the ConvertListToOrganizedList

    # create the metadata
    metadata = MetaData(OPERATORS_DICTIONARY)

    # convert the string to list
    convertor_string_to_list = StringToListConverter()
    metadata.equation_list = convertor_string_to_list.convert_string_to_list(
        equation)

    # create main convertor
    convertor = ConvertListToOrganizedList(metadata)
    assert convertor.create_organize_list() == expected, \
        "failed to check item: " + equation
