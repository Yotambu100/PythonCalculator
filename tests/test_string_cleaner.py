import pytest

from string_cleaner import *

LEGAL_WHITE_SPACES = {' ', '\t', '\n'}

TEST_DATA = [
    ("  ", ""),
    ("\t", ""),
    ("\n", ""),
    ("  \t  \n  \t", "")

]


@pytest.mark.parametrize("equation,expected_equation", TEST_DATA)
def test_clean_equation_from_legal_white_space(equation, expected_equation):

    assert remove_white_spaces(equation, LEGAL_WHITE_SPACES) \
           == expected_equation
