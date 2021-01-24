import pytest

from metadata import MetaData
from string_to_list_converter import StringToListConverter
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
    ("4+4", [4, '+', 4]),
    ("-(0-4)", ['-', '(', 0, '-', 4, ')']),
    ("4+3*5-3.3+1/2", [4, '+', 3, '*', 5, '-', 3.3, '+', 1, '/', 2]),
    ("6*4+2^5-3", [6, '*', 4, '+', 2, '^', 5, '-', 3]),
    ("2^3^4*2", [2, '^', 3, '^', 4, '*', 2]),
    ("322*53+2-2/2%98", [322, '*', 53, '+', 2, '-', 2, '/', 2, '%', 98])

]


@pytest.mark.parametrize("equation,expected", TEST_DATA)
def test_create_list_convertor(equation, expected):

    # create main convertor
    convertor = StringToListConverter()

    assert convertor.convert_string_to_list(equation) == expected, \
        "failed item: " + equation
