from equation_status_code import InvalidEquationCode
from string_to_list_converter import StringToListConverter


class StringValidator:
    """
    Class that responsible on checking the validation of the equation.
    the class preform several tests the equation as string and as
    list(different tests)
    """

    def __init__(self, metadata):

        # metadata hold important information about the equation
        self.metadata = metadata

        # The equation from the user as a string
        self.string_equation = metadata.equation_string

        # The equation from the user as a list
        self.list_equation = None

        # dictionary that link all the operators char as key and
        # their respectively operator class instance as value
        self.OPERATORS_DICTIONARY = metadata.OPERATORS_DICTIONARY

    def is_equation_valid(self):
        """
        The function preform a pre calculation validation tests on the
        equation to determine whether or not the program should try
        and solve the equation (the function find only pre calculations
        error like syntax error,missing bracket and ect' and not
        runtime errors like division by zero, complex number and more)
        :return:True if the equation pass successfully all the pre
        calculation tests
        """

        # setting the current invalid_equation_error_code to
        # valid (currently the equation is good/valid)
        self.metadata.invalid_equation_error_code = InvalidEquationCode.VALID

        # checking if the equation is empty
        # if true set the invalid_equation_error_code
        # accordingly(EMPTY_EQUATION) and return false
        if not self.string_equation:
            self.metadata.invalid_equation_error_code \
                = InvalidEquationCode.EMPTY_EQUATION
            return False

        # preform several validation tests on the equation as string
        # if true the equation passed successfully the first check
        # if false the equation is not valid and the function
        # return false
        if self._is_equation_valid_string_check():
            string_list_convertor = StringToListConverter()

            # convert the equation from string to list
            self.list_equation = string_list_convertor.convert_string_to_list(
                self.string_equation)

            # preform several more validation tests on the equation as
            # list  and return the result (different tests)
            return self._is_equation_valid_list_check()

        return False

    def _is_equation_valid_list_check(self):
        """
        The function runs operators location test and unnecessary
        brackets tests on the equation (as a list) to check if
        the equation is valid
        :return:True if the equation pass successfully the validation
         tests
        """
        return self._is_operators_and_operands_in_equation_valid() and \
               self._check_unnecessary_brackets()

    def _is_equation_valid_string_check(self):
        """
        The function runs syntax and brackets tests on the equation
        (as a string) to check if the equation is valid
        :return:True if the equation pass successfully the tests
        """
        return self._is_all_characters_valid() \
               and self._is_open_close_bracket_valid() \
               and self._check_decimal_point_validation()

    def _is_operators_and_operands_in_equation_valid(self):
        """
        # The function checks every char(number/brackets/operator) in
        the equation and test whether or not the char is in a valid
        position
        :return:True if all the characters in the equation are in valid
        position
        """

        # keeping track of the index of current char
        index_of_char = 0
        for char in self.list_equation:

            # if current char is number
            if isinstance(char, float):

                # if number is not valid at his position update the
                # invalid_equation_error_code to the corresponding
                # one and return false
                # if false continue to next char(increase index of
                # current char)
                if not self._is_number_valid_at_index(index_of_char):
                    self.metadata.invalid_equation_error_code \
                        = InvalidEquationCode.OPERATORS_OPERANDS_ERROR
                    return False

                index_of_char += 1

            # if current char is brackets
            # continue to next char(increase index of current char)
            elif char == '(' or char == ')':
                index_of_char += 1

            # if get to here current char must be operator
            # check if current operator is valid at his position(by
            # using the OPERATORS_DICTIONARY that hold an instance to
            # the current operator class and calling
            # is_operator_valid_at_index from that  instance)
            # if true continue to next char(increase index of
            # current char)
            elif self.OPERATORS_DICTIONARY[char].is_operator_valid_at_index(
                    self.list_equation,
                    index_of_char,
                    self.OPERATORS_DICTIONARY):

                index_of_char += 1

            # else means the char is not valid at his position so
            # update the invalid_equation_error_code to the
            # corresponding one and return false
            else:
                self.metadata.invalid_equation_error_code \
                    = InvalidEquationCode.OPERATORS_OPERANDS_ERROR
                return False

        # if all characters in the equation were valid at their position
        # return true
        return True

    def _is_open_close_bracket_valid(self):
        """
        The function checks if the open and close brackets in the
        equation are valid.
        meaning there is the same number of open and close brackets
        and before every close bracket there is at least one not close
        open bracket
        (unnecessary bracket is tested in other place)
        :return:True if the open and close brackets are valid in the
        equation
        """

        # Initializing the counter of open unclosed brackets to zero
        number_of_open_unclose_brackets = 0

        # scanning every char in the equation
        for character in self.string_equation:

            # if the char is open brackets
            if character == '(':
                # increase the counter by one
                number_of_open_unclose_brackets += 1

            # if the char is close brackets

            if character == ')':

                # decrease the counter by one
                number_of_open_unclose_brackets -= 1

                # check if counter is smaller than zero if true
                # there is close bracket without an unclosed open bracket
                # meaning the equation is invalid, save the
                # corresponding error and return false
                if number_of_open_unclose_brackets < 0:
                    self.metadata.invalid_equation_error_code = \
                        InvalidEquationCode.CLOSE_WITHOUT_OPEN_BRACKET

                    return False

        # after scanning all the equation if the counter is bigger
        # than zero there is an open bracket without a close one
        # meaning the equation is invalid, save the corresponding error
        # and return false
        if number_of_open_unclose_brackets > 0:
            self.metadata.invalid_equation_error_code = \
                InvalidEquationCode.TOO_MANY_OPEN_BRACKET
            return False

        # if got to here the counter is zero meaning for every
        # open bracket there is a close bracket meaning the open
        # close bracket test is valid, return true
        return True

    def _is_all_characters_valid(self):
        """
        The function check if the equation is build from only valid
        characters
        :return:True if the equation is build from only valid
        characters(number ,brackets, decimal point and operators)
        """

        # get all the allowed operator as set
        allowed_operator = set(self.OPERATORS_DICTIONARY.keys())

        # get all the allowed numbers, brackets and decimal point as set
        allowed_numbers_and_bracket = set('0123456789.()')

        # combine both sets into one
        allowed_chars = allowed_operator | allowed_numbers_and_bracket

        # if the equation is any sort of combination of all the allowed
        # characters(subset) return true
        # if not the equation is invalid, save the corresponding error
        # and return false
        if set(self.string_equation).issubset(allowed_chars):
            return True
        else:
            self.metadata.invalid_equation_error_code = \
                InvalidEquationCode.UNDEFINED_CHARACTERS
            return False

    def _check_unnecessary_brackets(self):
        """
        The function check whether or not the equation contain
        unnecessary brackets
        :return:True if the equation doesnt contain unnecessary brackets
        """

        # Stack that hold hold all the elements between every
        # unclosed bracket(every time a close bracket is found pop all
        # the element until open bracket include)
        equation_stack = []

        # scanning all the equation
        for current_char in self.list_equation:

            # if current char is close bracket check until the
            # first open bracket if those open bracket was unnecessary
            if current_char == ')':

                # if the last close open bracket was unnecessary
                # the equation is invalid, save the corresponding error
                # and return false
                if not self._is_last_bracket_necessary(equation_stack):
                    self.metadata.invalid_equation_error_code \
                        = InvalidEquationCode.UNNECESSARY_BRACKET
                    return False

            # else the char is not close bracket
            # push the current char to stack
            else:
                equation_stack.append(current_char)

        return True

    def _is_last_bracket_necessary(self, equation_stack):
        """
        The function check if the last open close bracket (that found
        in stack) is necessary
        :param equation_stack:Stack that hold all the elements between
        every unclosed bracket in the equation
        :return:True if the last onclose bracket that was in the
        stack was necessary
        """

        # if the top of the stack is open brackets
        # the brackets was unnecessary
        if equation_stack[-1] == '(':
            return False

        # if got to here the last brackets was necessary
        # pop all the element between the brackets (include the
        # bracket) and return true
        while equation_stack[-1] != '(':
            equation_stack.pop()

        equation_stack.pop()
        return True

    def _is_number_valid_at_index(self, index_of_number):
        """
        The function checks if the location of a number is valid
        based on his position in the equation and the elements
        adjacent to him
        :param index_of_number:The index of the number in the list
        :return:True if the number is valid at his index
        """

        # checking if number is at the edges of equation
        # if true,check only after/before index
        # (according if the index is at the start/end of list )
        if index_of_number == 0 \
                or index_of_number == len(self.list_equation) - 1:
            return self._is_number_valid_at_edge(index_of_number)

        char_before = self.list_equation[index_of_number - 1]
        char_after = self.list_equation[index_of_number + 1]

        # if char before is ')' or the char after is '('
        # the equation is invalid and return False(missing operator)
        if char_before == ')' or char_after == '(':
            return False

        return True

    def _is_number_valid_at_edge(self, index_of_number):
        """
        The function checks if the location of a number on the edges of
        the equation is valid based on his position in the
        equation and the elements adjacent to him
        :param index_of_number:The index of the number in the list
        :return:True if the number is valid at his index
        """

        # if the equation is only one element(number) return true
        if index_of_number == 0 \
                and index_of_number == len(self.list_equation) - 1:
            return True

        # if number at the start check only the char after him
        if index_of_number == 0:
            char_after = self.list_equation[index_of_number + 1]

            # after a number cant be a open bracket
            if char_after == '(':
                return False
            return True

        else:
            # if number at the end check only the char before him
            char_before = self.list_equation[index_of_number - 1]

            # before a number cant be a close bracket
            if char_before == ')':
                return False
            return True

    def _check_decimal_point_in_number(self):
        """
        The function check if there is no more than one decimal point
        per number
        :return:True if there is no more than one decimal point
        per number
        """

        # initialization the number of dot in one number counter
        number_of_dots_in_current_number = 0

        # scanning all the equation
        for current_char in self.string_equation:
            # if the current char is number dont do anything
            # and continue scanning the rest of the equation

            # if current char == '.'
            if current_char == '.':

                # increase the counter by one
                number_of_dots_in_current_number += 1

                # check if the counter is bigger than 1
                # if true there is more than one decimal point in number
                # meaning the equation is invalid, save the
                # corresponding error and return false
                if number_of_dots_in_current_number > 1:
                    self.metadata.invalid_equation_error_code = \
                        InvalidEquationCode.TOO_MANY_DOTS
                    return False

            # if current char is operator or brackets reseat the
            # counter to 0 and continue scanning the rest of the
            # equation
            elif current_char in self.OPERATORS_DICTIONARY or \
                    current_char == '(' or current_char == ')':
                number_of_dots_in_current_number = 0

        return True

    def _check_decimal_point_validation(self):
        """
        The function check if all the decimal points in the equation
        are valid
        (if there is not more than one decimal point per number and
        if there isn't an empty decimal point like .+3)
        :return:True if all the decimal points in the function are valid
        """

        return self._check_decimal_point_in_number() and \
               self._check_empty_decimal_points()

    def _check_empty_decimal_points(self):
        """
        The function check if all the decimal points in the equation
        arent empty like: ".+3" , ".+(3*2)"
        :return:True if all the decimal points in the function are
        not empty
        """

        # keeping track of the index of current char
        index_of_char = 0

        # scanning all the equation
        for current_char in self.string_equation:

            # if current char is equal to '.'
            # check if before or after him there is a number
            if current_char == '.':

                # check if the decimal point is at the start and at
                # the end of the equation
                # if true the decimal point is empty because there
                # isn't  a number adjacent to it meaning the equation
                # is invalid, save the corresponding error and
                # return false
                if index_of_char == 0 \
                        and index_of_char == len(self.string_equation) - 1:
                    self.metadata.invalid_equation_error_code = \
                        InvalidEquationCode.EMPTY_DECIMAL_POINT
                    return False

                # check if the decimal point is only at the start of
                # the equation if true check if the char after the
                # current char is not number
                elif index_of_char == 0:

                    # if the char after the current char is not number
                    # the decimal point is empty because there isn't
                    # a number adjacent to it meaning the equation
                    # is invalid, save the corresponding error and
                    # return false
                    if not self.string_equation[index_of_char + 1].isdigit():
                        self.metadata.invalid_equation_error_code = \
                            InvalidEquationCode.EMPTY_DECIMAL_POINT
                        return False

                # check if the decimal point is only at the end of
                # the equation if true check if the char before the
                # current char is not number
                elif index_of_char == len(self.string_equation) - 1:

                    # if the char before the current char is not number
                    # the decimal point is empty because there isn't
                    # a number adjacent to it meaning the equation
                    # is invalid, save the corresponding error and
                    # return false
                    if not self.string_equation[index_of_char - 1].isdigit():
                        self.metadata.invalid_equation_error_code = \
                            InvalidEquationCode.EMPTY_DECIMAL_POINT
                        return False

                # the decimal point is in the middle of the equation
                else:

                    # check if both of the adjacent chars are not
                    # numbers if true the decimal point is empty
                    # because there isn't  number adjacent to it
                    # meaning the equation is invalid,  save the
                    # corresponding error and return false
                    if not self.string_equation[index_of_char + 1].isdigit() \
                            and not \
                            self.string_equation[index_of_char - 1].isdigit():
                        self.metadata.invalid_equation_error_code = \
                            InvalidEquationCode.EMPTY_DECIMAL_POINT
                        return False
            # increasing the index of current if char
            index_of_char += 1

        return True
