import enum


class InvalidEquationCode(enum.Enum):
    """
    enum class that hold invalid code for all types of errors in equation
    """
    VALID = 1
    UNDEFINED_CHARACTERS = 2
    CLOSE_WITHOUT_OPEN_BRACKET = 3
    EMPTY_EQUATION = 4
    TOO_MANY_OPEN_BRACKET = 5
    OPERATORS_OPERANDS_ERROR = 6
    TOO_MANY_DOTS = 7
    UNNECESSARY_BRACKET = 8
    DIVISION_BY_ZERO = 9
    FACTORIAL_ON_NEGATIVE_NUMBER = 10
    FACTORIAL_ON_DECIMAL_NUMBER = 11
    NUMBER_TOO_BIG = 12
    COMPLEX_NUMBER = 13
    EMPTY_DECIMAL_POINT = 14
