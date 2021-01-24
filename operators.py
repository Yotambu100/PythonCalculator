import enum
from abc import ABC, abstractmethod
from calculation_result import CalculationResult
from equation_status_code import InvalidEquationCode


# enum that state the operator position relative to the operand
class OperatorPosition(enum.Enum):
    RIGHT_OF_NUMBER = 1
    LEFT_OF_NUMBER = 2
    BETWEEN_NUMBERS = 3


class OperatorAbstract(ABC):
    """
    Blueprint for every operator.
    in order to add new operator just create a new class that inherit from
    this class, fill/Initialize the function and properties according to the
    new operator and add it the the OPERATORS_DICTIONARY
    """

    @abstractmethod
    def calculate(self, first_number, second_number):
        """
        This function does the calculation of the operator
        (if the operator is one number operator one of the numbers
        will be automatically zero - if the operator is left to operand
        first_number will be zero and if the operator is right to
        operand second_number will be zero)

        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold the
        error code) and the calculation result
        """
        pass

    @property
    @abstractmethod
    def is_operator_two_number_operator(self):
        """
        The property declares if the operator is two number operator or
        one
        :return:True if the operator is two number operator
        """
        pass

    @property
    @abstractmethod
    def operator_power(self):
        """
        The property declares the operator power(meaning his priority)
        :return:The operator priority
        """
        pass

    @property
    @abstractmethod
    def operator_position(self):
        """
        The property declares the operator position relative to the operand
        :return:enum stating the operator position relative to the
        operand (RIGHT_OF_NUMBER, LEFT_OF_NUMBER, BETWEEN_NUMBERS )
        """
        pass

    @property
    @abstractmethod
    def is_chaining(self):
        """
        The property declares if the operator is chaining or not
        :return:True if the operator is chaining
        """
        pass

    @abstractmethod
    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        """
        This function check if the location of an operator is valid
        based on his position in the equation and the elements adjacent
        to him
        (The abstract class provide an implementation to this function
        for common operators[two number operator, not chaining] like:
        '+','/','*','%','@','^','$','&' )
        :param list_equation:The list the operator was found in
        :param operator_index:The index of the operator in the list
        :param OPERATORS_DICTIONARY:Dictionary that link all the
        operators char as key and their respectively operator class
        instance as value
        :return:True if the operator is valid at his index
        """

        # if the operator is at the start or the end of the equation
        # return false
        if operator_index == 0 or operator_index == len(list_equation) - 1:
            return False

        # save the element before and after the operator
        char_before_operator = list_equation[operator_index - 1]
        char_after_operator = list_equation[operator_index + 1]

        # check if the operator can be between the elements he is between
        # if he can return True else Return False
        if is_char_before_operator_valid(char_before_operator,
                                         self.operator_power,
                                         OPERATORS_DICTIONARY):
            if is_char_after_index_valid(char_after_operator,
                                         OPERATORS_DICTIONARY):
                return True

        return False


class Plus(OperatorAbstract):
    operator_power = 1
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number+second_number
        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()
        try:
            # try do the calculation
            calculation_data.result = first_number + second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)

        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Minus(OperatorAbstract):
    operator_power = 1
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.LEFT_OF_NUMBER
    is_chaining = True

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number-second_number(if the minus
        is a sign the first number will automatically be zero)
        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()
        try:

            # try do the calculation
            calculation_data.result = first_number - second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)

        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):

        # if the minus is at the end of the equation return false
        # (minus cant be at the end)
        if operator_index == len(list_equation) - 1:
            return False

        # save the element after the minus
        char_after_minus = list_equation[operator_index + 1]

        # if the element after the minus is close bracket return false
        # (close bracket can be after minus)
        if char_after_minus == ')':
            return False

        # if the element after the minus is number or open bracket or
        # a chaining left of number operator return true (those are the only
        # options from an element after minus) else return false
        if isinstance(char_after_minus, float) \
                or char_after_minus == '(' \
                or (OPERATORS_DICTIONARY[char_after_minus].is_chaining
                    and OPERATORS_DICTIONARY[
                        char_after_minus].operator_position ==
                    OperatorPosition.LEFT_OF_NUMBER):
            return True

        return False


class Multiplication(OperatorAbstract):
    operator_power = 2
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number*second_number
        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()
        try:
            # try do the calculation
            calculation_data.result = first_number * second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Division(OperatorAbstract):
    operator_power = 2
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number/second_number
        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()

        # check if second number(divider) equal to zero
        # if true the equation is invalid, save the corresponding error
        # and changes the calculation_data.is_successful to false
        # (flag that indicate if the calculation was successful or not)
        if second_number == 0:
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.DIVISION_BY_ZERO

            return calculation_data
        try:
            # try do the calculation
            calculation_data.result = first_number / second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Power(OperatorAbstract):
    operator_power = 3
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number^second_number
        :param first_number: The number to the left of the operator
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()

        try:
            # try do the calculation
            calculation_data.result = first_number ** second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf
        # or complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Negation(OperatorAbstract):
    operator_power = 6
    is_operator_two_number_operator = False
    operator_position = OperatorPosition.LEFT_OF_NUMBER
    is_chaining = True

    def calculate(self, first_number, second_number):
        """
        This function calculate -second_number
        :param first_number: The number to the left of the
        operator(automatically zero)
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()

        try:
            # try do the calculation
            calculation_data.result = -second_number
        except OverflowError:
            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)

        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):

        # if the negation at the end of the equation return false
        if operator_index == len(list_equation) - 1:
            return False

        # save the element after the negation
        char_after_negation = list_equation[operator_index + 1]

        # if the negation is at the start
        # if true check only the element after it
        # if the element after it is valid return true else false
        if operator_index == 0:
            if self._is_char_after_negation_valid(char_after_negation,
                                                  OPERATORS_DICTIONARY):
                return True
            else:
                return False

        # save the element before the negation
        char_before_index = list_equation[operator_index - 1]

        # if the element before the negation is not valid
        # return false
        if not self._is_char_before_negation_valid(char_before_index,
                                                   OPERATORS_DICTIONARY):
            return False

        # if got to here the element before the negation is valid
        # so check the element after if valid return true if not false
        if self._is_char_after_negation_valid(char_after_negation,
                                              OPERATORS_DICTIONARY):
            return True
        else:
            return False

    def _is_char_after_negation_valid(self, char_after_negation,
                                      OPERATORS_DICTIONARY):
        """
        This function check if the the negation is valid based
        on the char after it
        :param char_after_negation: the char after the negation
        :param OPERATORS_DICTIONARY:Dictionary that link all the
        operators char as key and their respectively operator class
        instance as value
        :return:True if the negation is valid based on the char
        after it
        """

        # if the char after the negation is number return True
        # (after negation can be number)
        if isinstance(char_after_negation, float):
            return True

        # if the char after the negation is close bracket return True
        # (after negation can be close bracket)
        if char_after_negation == '(':
            return True

        # if the char after the negation is open bracket return False
        # (after negation cant be open bracket)
        if char_after_negation == ')':
            return False

        # if get to here the char after must be operator
        operator_after_negation = OPERATORS_DICTIONARY[char_after_negation]

        # if the operator after is chaining and left of number return
        # true else return false
        # (the only condition an operator can be after negation is if
        # he is chaining and he is left to number operator)
        if operator_after_negation.is_chaining \
                and operator_after_negation.operator_position == \
                OperatorPosition.LEFT_OF_NUMBER:
            return True

        return False

    def _is_char_before_negation_valid(self, char_before_negation,
                                       OPERATORS_DICTIONARY):

        """
        This function check if the the negation is valid based
        on the char before it
        :param char_before_negation: the char before the negation
        :param OPERATORS_DICTIONARY:Dictionary that link all the
        operators char as key and their respectively operator class
        instance as value
        :return:True if the negation is valid based on the char
        before it
        """

        # if the char before the negation is number return False
        # (before negation cant be number)
        if isinstance(char_before_negation, float) \
                or char_before_negation == ')':
            return False

        # if the char before the negation is open bracket return True
        # (before negation can be open bracket)
        if char_before_negation == '(':
            return True

        # if get to here the char after must be operator
        operator_before_negation = OPERATORS_DICTIONARY[char_before_negation]

        # if the operator before the negation is {two number operator
        # and his power smaller then the negation} or {the operator is
        # chaining and he is left of number operator} return True
        # (those are the only two scenarios where operator can be
        # before negation)
        if (operator_before_negation.is_operator_two_number_operator
            and operator_before_negation.operator_power < self.operator_power) \
                or (operator_before_negation.is_chaining
                    and operator_before_negation.operator_position ==
                    OperatorPosition.LEFT_OF_NUMBER):
            return True

        return False


class Modulo(OperatorAbstract):
    operator_power = 4
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):
        """
        This function calculate first_number % second_number
        :param first_number: The number to the left of the
        operator(automatically zero)
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()

        # check if second number(divider) equal to zero
        # if true the equation is invalid, save the corresponding error
        # and changes the calculation_data.is_successful to false
        # (flag that indicate if the calculation was successful or not)
        if second_number == 0:
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.DIVISION_BY_ZERO

            return calculation_data
        try:
            # try do the calculation
            calculation_data.result = first_number % second_number
        except OverflowError:

            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Factorial(OperatorAbstract):
    operator_power = 6
    is_operator_two_number_operator = False
    operator_position = OperatorPosition.RIGHT_OF_NUMBER
    is_chaining = True

    def calculate(self, first_number, second_number):
        """
        This function calculate the factorial of first_number
        :param first_number: The number to the left of the
        operator(automatically zero)
        :param second_number:The number to the right of the operator
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold
        the error code) and the calculation result
        """

        # create the CalculationResult
        calculation_data = CalculationResult()

        # check if second first_number is negative or Decimal number
        # if true the equation is invalid, save the corresponding error
        # and changes the calculation_data.is_successful to false
        # (flag that indicate if the calculation was successful or not)
        if not self._pre_check_calculation(calculation_data, first_number):
            return calculation_data

        try:
            # try do the calculation
            calculation_data.result = 1.0
            for i in range(1, int(first_number) + 1):
                calculation_data.result *= i

        except OverflowError:
            # if get to here the number is too  big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):

        # if the factorial is at the start of the equation return false
        # (factorial cant be at the start)
        if operator_index == 0:
            return False

        # save the element before the factorial
        char_before_factorial = list_equation[operator_index - 1]

        # if the factorial at the end check only the char before
        if operator_index == len(list_equation) - 1:
            if self._is_char_before_factorial_valid(char_before_factorial,
                                                    OPERATORS_DICTIONARY):
                return True
            else:
                return False

        # save the element after the factorial
        char_after_factorial = list_equation[operator_index + 1]

        # if the char before the factorial is valid and the
        # the char after the factorial is close bracket or
        # operator with less or equal power return true
        if self._is_char_before_factorial_valid(char_before_factorial,
                                                OPERATORS_DICTIONARY):

            if char_after_factorial == ')' or \
                    (char_after_factorial in OPERATORS_DICTIONARY
                     and OPERATORS_DICTIONARY[
                         char_after_factorial].operator_power
                     <= self.operator_power):
                return True

        return False

    def _pre_check_calculation(self, calculation_data, first_number):
        """
        This function checks if its legal to do a factorial on
        first_number
        :param calculation_data:Object that hold whether or not the
        calculation was successful(if it was unsuccessful it will
        hold the error code) and the calculation result
        :param first_number:The number wants to do factorial on
        :return:True if its valid to do factorial on first_number
        """

        # if first_number is a decimal number
        # the equation is invalid, save the corresponding error
        # and changes the calculation_data.is_successful to false
        # (can do factorial on only integer)
        if not first_number.is_integer():
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.FACTORIAL_ON_DECIMAL_NUMBER

        # if first_number is a negative
        # the equation is invalid, save the corresponding error
        # and changes the calculation_data.is_successful to false
        # (can do factorial on only positive numbers)
        if first_number < 0:
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.FACTORIAL_ON_NEGATIVE_NUMBER

        return calculation_data.is_successful

    def _is_char_before_factorial_valid(self, char_before_negation,
                                        OPERATORS_DICTIONARY):
        """
        This function check if the element before the factorial can be
        there in a validly way
        :param char_before_negation:The element before the factorial
        :param OPERATORS_DICTIONARY:Dictionary that link all the
        operators char as key and their respectively operator class
        instance as value
        :return:True if the element before the factorial can be there
        """

        # Factorial cant be after open bracket
        if char_before_negation == '(':
            return False

        # Factorial can be after close bracket or a number
        if isinstance(char_before_negation, float) \
                or char_before_negation == ')':
            return True

        # if get to here the char before negation must be an operator
        operator_before_factorial = OPERATORS_DICTIONARY[char_before_negation]

        # if the operator before the factorial is an operator
        # with greater or equal power and chaining return true
        # (the only operator that can be before the factorial is
        # operator with greater or equal power and chaining)
        if operator_before_factorial.is_chaining \
                and operator_before_factorial.operator_position \
                == OperatorPosition.RIGHT_OF_NUMBER \
                and operator_before_factorial.operator_power \
                >= self.operator_power:
            return True

        return False


class Average(OperatorAbstract):
    operator_power = 5
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):

        # create the CalculationResult
        calculation_data = CalculationResult()
        try:

            # try do the calculation
            calculation_data.result = (first_number + second_number) / 2

        except OverflowError:
            # if get to here the number is too big meaning
            # the equation is invalid, save the corresponding error
            # and changes the calculation_data.is_successful to false
            # (flag that indicate if the calculation was successful
            # or not)
            calculation_data.is_successful = False
            calculation_data.invalid_equation_code = \
                InvalidEquationCode.NUMBER_TOO_BIG

        # general check on the result (check if number is inf ,-inf or
        # complex)
        is_valid_result(calculation_data)
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Maximum(OperatorAbstract):
    operator_power = 5
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):

        # create the CalculationResult
        calculation_data = CalculationResult()

        # try do the calculation
        calculation_data.result = \
            first_number if first_number > second_number else second_number
        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


class Minimum(OperatorAbstract):
    operator_power = 5
    is_operator_two_number_operator = True
    operator_position = OperatorPosition.BETWEEN_NUMBERS
    is_chaining = False

    def calculate(self, first_number, second_number):

        # create the CalculationResult
        calculation_data = CalculationResult()

        # try do the calculation
        calculation_data.result = \
            first_number if first_number < second_number else second_number

        return calculation_data

    def is_operator_valid_at_index(self, list_equation, operator_index,
                                   OPERATORS_DICTIONARY):
        return super().is_operator_valid_at_index(list_equation,
                                                  operator_index,
                                                  OPERATORS_DICTIONARY)


def is_char_before_operator_valid(char_before_operator, current_operator_power,
                                  OPERATORS_DICTIONARY):
    """
    This function check if the element before the operator can be there in a
    validly way
    :param char_before_operator:The element before the operator
    :param current_operator_power:The operator checking power (priority)
    :param OPERATORS_DICTIONARY:Dictionary that link all the operators
    char as key and their respectively operator class instance as value
    :return:True if the element before the operator can be there
    """

    # if the element before the operator is number or close brackets
    # return true(before a common operators can be number or close brackets)
    if isinstance(char_before_operator, float) or char_before_operator == ')':
        return True

    # if the element before is an open bracket return false
    # (before a common operators cant be open brackets)
    if char_before_operator == '(':
        return False

    # if got to here the element before the operator is an operator
    operator_before_index = OPERATORS_DICTIONARY[char_before_operator]

    # if the operator before is one number operator that his power is greater
    # or equal to current operator and he is right of number operator return
    # true
    # (if not return false because this is the only condition that a operator
    # can be before a common operator)
    if not operator_before_index.is_operator_two_number_operator \
            and operator_before_index.operator_power >= \
            current_operator_power \
            and operator_before_index.operator_position \
            == OperatorPosition.RIGHT_OF_NUMBER:
        return True

    return False


def is_char_after_index_valid(char_after_operator, OPERATORS_DICTIONARY):
    """
    This function check if the element after the operator can be there
    in a validly way
    :param char_after_operator:The element after the operator
    :param OPERATORS_DICTIONARY:Dictionary that link all the operators
    char as key and their respectively operator class instance as value
    :return:True if the element after the operator can be there
    """

    # if the element after the operator is number or open brackets
    # return true(before a common operators can be number or open brackets)
    if isinstance(char_after_operator, float) or char_after_operator == '(':
        return True

    # if the element after is an close bracket return false
    # (before a common operators cant be close brackets)
    if char_after_operator == ')':
        return False

    # if got to here the element after the operator is an operator
    operator_after_index = OPERATORS_DICTIONARY[char_after_operator]

    # if the operator after is chaining operator and not right of number
    # return true(that is the only condition that a operator can be
    # after common operators )
    if operator_after_index.is_chaining \
            and not operator_after_index.operator_position == OperatorPosition \
            .RIGHT_OF_NUMBER:
        return True

    return False


def is_valid_result(calculation_data):
    """
    The function check if the calculation result is valid
    :param calculation_data:Object that hold whether or not the
    calculation was successful(if it was unsuccessful it will hold the
    error code) and the calculation result
    """

    # if the calculation result is inf or -inf
    # the equation is invalid, save the corresponding error
    # and changes the calculation_data.is_successful to false (flag that
    # indicate if the calculation was successful or not)
    if calculation_data.result == float('inf') \
            or calculation_data.result == float('-inf'):

        calculation_data.is_successful = False
        calculation_data.invalid_equation_code = \
            InvalidEquationCode.NUMBER_TOO_BIG

    # if the calculation result is complex number
    # the equation is invalid, save the corresponding error
    # and changes the calculation_data.is_successful to false (flag that
    # indicate if the calculation was successful or not)
    elif isinstance(calculation_data.result, complex):
        calculation_data.is_successful = False
        calculation_data.invalid_equation_code = \
            InvalidEquationCode.COMPLEX_NUMBER
