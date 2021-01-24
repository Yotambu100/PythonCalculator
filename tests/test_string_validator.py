import pytest

from metadata import MetaData
from string_cleaner import remove_white_spaces
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

LEGAL_WHITE_SPACES = {' ', '\t', '\n'}

TEST_DATA = [
    # syntax error
    ("5**5", False),
    (")4+4(", False),
    ("(5*4)8", False),
    ("2(1*4)", False),
    ("4-+4", False),
    ("-w4", False),
    ("5**3", False),
    ("2!!2", False),
    ("(3+3", False),
    ("2-2)", False),
    ("(3+3)*6/1)", False),
    ("5*+5", False),
    ("-((5", False),
    ("5..5", False),
    (".", False),
    ("((5+5))", False),
    ("5!(5)", False),
    ("(~~)", False),
    ("5*.", False),
    ("5$1~", False),
    ("())", False),
    ("{]", False),
    ("!", False),
    ("~", False),
    ("-", False),
    ("5-~--~-~", False),

    # spacial cases
    ("2..2+1", False),
    ("2.(2.2+1)+1", False),
    ("(+3-2)", False),
    ("(3+3*)", False),
    ("4~-~-2", False),
    ("4~~2", False),
    ("4..2", False),
    ("4.2.2", False),
    ("2-^(1+1)", False),
    (".+3", False),
    ("3+.", False),
    ("3+.+3", False),
    ("((3+1))", False),
    ("(((3*2)+1))", False),

    # Gibberish syntax
    ("4+eed+-dk9d", False),

    # empty equation
    ("", False),
    ("\t", False),
    ("\n", False),
    (" ", False),

    # valid equation
    ("3/3.2+1", True),
    ("4-4", True),
    ("--4", True),
    ("2!!", True),
    ("-2", True),
    ("~2", True),
    ("-~-~-2", True),
    ("4-~-~-2", True),
    ("2^-(1+1)", True),
    ("(~2)", True),
    ("(~(~2))", True),
    (".4+1", True),
    ("12.+1", True),
    ("(3)", True),
    ("(-3)", True),

    # Valid long equation
    ("---6&22%(2+6-5)^2-2&21$221@0", True),
    ("9*~(6+6)+2^2", True),
    ("----(8*--8)$5+2%456+9*9*~(6+6)+2^(-(1+1))", True),
    ("----~4+67*2-4522/221+(2&23*22%3^2)-7*2@4", True),
    ("((2+4-6^~2-4+2)/(2+3^2/5&2@56)+76-~(4!))", True),
    ("18-6^2+5%4$3+2+4+5+6-------9+7&5/3.2%4.2", True),
    ("0!+-1*2/3^4%5&6$7@~8", True),
    ("(1+2)^((-1+~2)*-1)!+(3-1)!", True),
    ("((6+6)+(6+6))", True),
    ("~((88/23*2.2)^3&(5!+---6^3))", True),
    ("14$5%2&4+4+4-7.7+(5*3$2)!", True),
    ("7&8*22^3!-7^3+((22%2*7)+3$5^3&~7)", True),
    ("005*2^2&2-7&88+224@26-(43-44+66&2----45*(321&2))", True),
    ("(--(--(--(--(4+4)))))", True),
    ("~(123@((145*2/4%6-6/7)@(3^5-9000)))", True),
    ("8-7^2+4%6!+(5$9+(6^7-10&9%2))", True),
    ("123/86+996-22*77$(6^2%4-(88---7+5^3*2$3^7))", True),
    ("4$55^27*22&44*(23$2^2&43*6&(65^2+2--6))", True),
    ("5!-52&5*2-((2*2)+45^0.5+~2)", True),
    ("77^2*6%4$3@678*(2^7&22^2-(7^2)---3+66&6)", True),
    ("55%66$78^2+5----65^2*((3$5^7@555)+6^2&12^2)-2", True),
    ("3&~2*4", True),
    ("7&8*22^3!-7^3+((22%2*7)+3$5^3&~7)", True),
    ("~~~----~-~---~--~~~~~----~-~-~2323", True),
    ("24%12^2-7*9&(2+3-4+6$22--8--~((9+8)!))", True),
    ("5!-52&5*2-((2*2)+45^5+~2+2)", True),
    ("87^3%2&66@45%((22%4$2^2)+7*6!)^~2*6", True),
    ("24%12^2-7*9&(2+3-4+6$22--8--~((9+8)!))", True),
    ("87^3%2&66@45%((22%4$2^2)+7*6!)^~2*6", True),
    ("4--~~~3+22!+4--~~(33+6^2-~(5+7)+2)", True)
]


@pytest.mark.parametrize("equation,is_expected_valid", TEST_DATA)
def test_is_equation_valid(equation, is_expected_valid):
    # Set up validation object
    metadata = MetaData(OPERATORS_DICTIONARY)
    # handle the legal white spaces
    metadata.equation_string = remove_white_spaces(equation,
                                                   LEGAL_WHITE_SPACES)
    sv = StringValidator(metadata)
    assert sv.is_equation_valid() == is_expected_valid
