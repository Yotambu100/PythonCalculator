from equation_status_code import InvalidEquationCode


class StringToListConverter:
    """
    Class that responsible on converting the equation from string to
    list
    """

    def __init__(self):

        # the equation that will be converted to list
        self.equation_string = None

        # the equation as list
        self.equation_list = None

    def convert_string_to_list(self, equation_string):

        # saving the equation in the class
        self.equation_string = equation_string

        # initializing the new list and the index of current char
        self.equation_list = []
        index_of_current_char = 0

        # scanning all the equation
        while index_of_current_char < len(self.equation_string):

            # saving the char working on currently
            current_char = self.equation_string[index_of_current_char]

            # if the current char is number or decimal point
            # add the whole number to the new list as one element
            # and change the index to the next element after the
            # whole number
            if current_char.isdigit() or current_char == '.':
                index_of_current_char = self._add_new_number(
                    index_of_current_char)

            # else the current char is operator or brackets
            # add them to the new list and increase the index
            else:
                self.equation_list.append(
                    self.equation_string[index_of_current_char])
                index_of_current_char += 1

        # return the new list
        return self.equation_list

    def _add_new_number(self, index_of_starting_number):
        """
        The function gets an index to a start of a number(the start of
        a number can be number or decimal point) and add the full
        number to the new list(because the equation is given as a
        string every digit in a multi-digit number will be saved
        in different index in the string)
        :param index_of_starting_number:The start index of a number in
        the string
        :return:The index in the string of the next element after the
        whole number
        """

        # initializing the index of what will be the next element in
        # string
        end_index = index_of_starting_number + 1

        # scanning the equation and increasing the end_index until he
        # passes the number currently working on
        while len(self.equation_string) > end_index and (
                self.equation_string[end_index].isdigit()
                or self.equation_string[end_index] == '.'):
            end_index += 1

        # adding the whole number to the list
        self.equation_list.append(float(
            self.equation_string[index_of_starting_number:end_index]))

        # returning the index of the next element
        return end_index
