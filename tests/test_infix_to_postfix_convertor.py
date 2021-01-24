import pytest

from infix_to_postfix_convertor import InfixToPostfixConvertor
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
    ("4+4", [4, 4, '+']),
    ("-(0-4)", [0, 4, '-', '-']),
    ("4-(0-(-5$7))", [4, 0, 5, 7, '$', '-', '-', '-']),
    ("6*4+2^5-3", [6, 4, '*', 2, 5, '^', '+', 3, '-']),
    ("2^3^4*2", [2, 3, '^', 4, '^', 2, '*'])

]


@pytest.mark.parametrize("equation,expected", TEST_DATA)
def test_create_postfix_list_convertor(equation, expected):
    # Set up the InfixToPostFixConvertor

    # create the metadata
    metadata = MetaData(OPERATORS_DICTIONARY)

    # convert the string to list
    convertor_string_to_list = StringToListConverter()
    metadata.equation_list = convertor_string_to_list.convert_string_to_list(
        equation)

    # create main convertor
    convertor = InfixToPostfixConvertor(metadata.equation_list,
                                        OPERATORS_DICTIONARY)
    assert convertor.infix_to_postfix() == expected, "failed item: " + equation
