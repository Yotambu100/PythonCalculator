from operators import OperatorPosition


class ConvertListToOrganizedList:
    """
    class that responsible on converting the List to
    organized list. Full explanation about the organized list is in
    the doc
    """

    def __init__(self, metadata):

        # stack that holds the bracket's depth needs to add
        # closing bracket
        self.bracket_stack = None

        # stack that holds the bracket's depth that was
        # already found
        self.number_in_bracket_stack = None

        # metadata holds important information about the equation
        self.metadata = metadata

        # dictionary that link all the operators char as key and
        # their respectively operator class instance as value
        # i.e: "+" -> Plus (class)
        self.OPERATORS_DICTIONARY = metadata.OPERATORS_DICTIONARY

        # New organized list. List is being created after applying new
        # change
        self.organized_list = metadata.equation_list

    def _get_sorted_operators_list(self):
        """
        The function create a sorted (ascending by the operator_power)
        list of tuples contains (operator_power, operator_char,
        operator_object)
        :return:The new sorted list
        """
        operators_list = list(self.OPERATORS_DICTIONARY.keys())
        operators_list = [(self.OPERATORS_DICTIONARY[i].operator_power, i,
                           self.OPERATORS_DICTIONARY[i])
                          for i in operators_list]
        operators_list.sort()
        return operators_list

    def create_organize_list(self):
        """
        This function organizes the list by adding zero and brackets as needed.
        The function creates new organized list where every
        time there is an operators chain from left to right, it adds open
        bracket and zero before the chaining operator and close bracket before
        an operator with smaller or equal power only after passing a
        number.
        Every time there is an operators chain from right to left it adds
        zero to the right of the operators chain (see detailed
        explanation at the doc)
        for example 3-~-~4+3! ==>> 3-(0~(0-(0~4)))+3!0
        :return: New organized list
        """

        # get an operators_list that contain
        # (operator_power, operator_char, operator_object)
        # the list is sorted by the operator's power from the lowest
        # power operator to the highest. Keeping this order - lowest to
        # highest - is important in order for this algorithm to work)
        operators_list = self._get_sorted_operators_list()

        # for every chained left to right operator call
        # _handle_left_chained_operators (chained_operators is the tuple
        # from the operators_list. chained_operators[1] is the operator
        # char and chained_operators[2] is the operator instance
        for operator_char in (chained_operators[1] for chained_operators in
                              operators_list if
                              chained_operators[2].is_chaining
                              and chained_operators[2].operator_position
                              == OperatorPosition.LEFT_OF_NUMBER):
            self.organized_list = self._handle_left_chained_operators(
                operator_char)

        # for every chained right to left operator call
        # _handle_right_chained_operators (chained_operators is the tuple
        # from the operators_list. one_number_operators_right[1] is the
        # operator char and one_number_operators_right[2] is
        # the operator instance
        for operator_char in (one_number_operators_right[1] for
                              one_number_operators_right in
                              operators_list if
                              one_number_operators_right[2].is_chaining
                              and one_number_operators_right[
                                  2].operator_position
                              == OperatorPosition.RIGHT_OF_NUMBER):
            self.organized_list = self._handle_right_chained_operators(
                operator_char)

        return self.organized_list

    def _put_all_remaining_bracket_in_list(self, new_list):
        """
        The function put all the reminding brackt that are left in the
        bracket_stack in te new list
        :param new_list:The new organized list
        """

        # until the bracket_stack is empty
        # add close bracket and pop the stack
        while self.bracket_stack:
            new_list.append(')')
            self.bracket_stack.pop()

    def _handle_close_bracket_char(self, current_number_of_bracket, new_list):
        """
        The function add close bracket if there is close brackets needed
        to be added at the current_number_of_bracket(before decreasing
        by 1) than it add the close bracket itself and finally
        it add that a number was found in current_number_of_bracket-1
        :param new_list:The new organized list
        """

        # add close bracket if there is an open unclosed bracket at the
        # same depth (current_number_of_bracket is equal)
        self._add_close_bracket_if_needed(current_number_of_bracket, new_list)
        new_list.append(')')

        # add that a number was found in current_number_of_bracket
        # (only if needed)
        self._number_found_in_current_bracket(current_number_of_bracket - 1)

    def _handle_operator(self, left_chained_operator, current_operator_char,
                         operator_index,
                         new_list,
                         current_number_of_bracket, equation_list):
        """
        The function check if the operator that was found is the
        operator that is currently chaining or if his power is
        bigger than the power of the operator currently chaining and
        add it to the list accordingly(every situation needs to be
         handle differently)
        :param left_chained_operator:The chaining operator(the operator
        that the currently chaining)
        :param current_operator_char:The operator that was reached
        :param operator_index:The index of the operator that was reached
        :param new_list:The new organized list
        :param current_number_of_bracket:The Current depth of current
        brackets
        :param equation_list:The original list
        :return:
        """

        current_operator = self.OPERATORS_DICTIONARY[current_operator_char]

        # if the operator that was found is the left_chained_operator
        # (the operator that the function chaining) call the
        # _handle_current_working_operator that determine if current
        # operator is chaining in this instance and add the operator
        # to the organized list differently based on is location and if
        # he is chaining
        if current_operator_char == left_chained_operator:
            self._handle_current_working_operator(operator_index, new_list,
                                                  equation_list,
                                                  current_number_of_bracket,
                                                  left_chained_operator)
        else:

            # if the power of the operator that was found is bigger
            # than the power of the operator that is currently chaining
            # only add the operator
            if current_operator.operator_power > self.OPERATORS_DICTIONARY[
                left_chained_operator].operator_power:
                new_list.append(current_operator_char)

            else:
                # else check if need/can add close bracket and then
                # add the operator (the close bracket can be added
                # only before operators with smaller or equal power)
                self._add_close_bracket_if_needed(current_number_of_bracket,
                                                  new_list)
                new_list.append(current_operator_char)

    def _handle_current_working_operator(self, current_operator_index,
                                         new_list,
                                         equation_list,
                                         current_number_of_bracket,
                                         left_chained_operator):
        """
        The function check if in this instance the current operator is
        chaining and add it to the list differently based on it and
        based on the location of it in the equation
        :param current_operator_index: The index of the current operator
        :param new_list: The new organized list
        :param equation_list: The original list
        :param current_number_of_bracket: The Current depth in the
        brackets
        :param left_chained_operator: The operator that was found and
        currently working on
        """

        # if the operator was found at the start of the equation or
        # after open bracket add to the new organized list only zero
        # before the operator (no need to add bracket)
        if current_operator_index == 0 or equation_list[ \
                current_operator_index - 1] == '(':
            new_list.append(0.0)
            new_list.append(left_chained_operator)

        # if the operator was found after an operator that is not
        # right of number add to the new organized list open bracket
        # zero the chaining operator and add to the bracket_stack
        # the current number of bracket (if the operator was found
        # after a not right of number operator the current operator is
        # chaining so add "(0" and than the chaining operator and than
        # add to the bracket_stack that a close bracket should be add
        # at the current_number_of_bracket)
        elif equation_list[current_operator_index - 1] \
                in self.OPERATORS_DICTIONARY and not \
                self.OPERATORS_DICTIONARY[equation_list[
                    current_operator_index - 1]].operator_position \
                == OperatorPosition.RIGHT_OF_NUMBER:

            self.bracket_stack.append(current_number_of_bracket)
            new_list.append('(')
            new_list.append(0.0)
            new_list.append(left_chained_operator)
        else:
            # else the current operator is after a number
            # meaning the operator is not chaining at this instance
            # so add close bracket if needed(close brackets are added
            # if there was a number after the chaining operator and
            # right before an operator with equal or smaller power)
            # and then add the operator to the new organized list
            self._add_close_bracket_if_needed(current_number_of_bracket,
                                              new_list)
            new_list.append(left_chained_operator)

    def _number_found_in_current_bracket(self, current_number_of_bracket):
        """
        The function add that a number was found
        in current_number_of_bracket only if there is need(meaning the
        there is a close bracket waiting to be put in the same
        bracket depth as current)
        :param current_number_of_bracket:The depth of the current number
        in bracket
        """

        # if the bracket_stack is not empty continue checking
        # (meaning there is open bracket waiting to be closed)
        if self.bracket_stack:

            # if the top of bracket_stack is equal to
            # current_number_of_bracket (meaning the number is in the
            # same depth of the waiting to be closed open bracket)
            # and {the number_in_bracket_stack is empty or the top is
            # not equal to current_number_of_bracket} (meaning a
            # number was yet to be added to this depth)
            # add that a number is in that depth (by pushing into the
            # stack of number_in_bracket_stack)
            if self.bracket_stack[-1] == current_number_of_bracket \
                    and (not self.number_in_bracket_stack
                         or self.number_in_bracket_stack[
                             -1] != current_number_of_bracket):
                self.number_in_bracket_stack.append(current_number_of_bracket)

    def _add_close_bracket_if_needed(self, current_number_of_bracket,
                                     new_list):
        """
        The function add close bracket to the new organized list if the
        current_number_of_bracket is equal to the depth of the bracket
        needing to be closed and a number was found before in the same
        depth
        :param current_number_of_bracket:The current depth of the
        bracket
        :param new_list:The new organized list
        """

        # if both stacks are not empty and the top of bracket stack is
        # equal to the top of number_in_bracket_stack (meaning there
        # was a number in the same depth as an open waiting to be
        # closed bracket) and the top of bracket stack is equal to
        # the current_number_of_bracket (meaning the open unclosed
        # bracket is at the same depth as current depth)
        # pop the number_in_bracket_stack to remove the number in the
        # same depth and until the top of bracket_stack is not the same
        # as current depth pop from bracket_stack and add close bracket
        # to the new organized list
        if self.bracket_stack and self.number_in_bracket_stack:
            if self.bracket_stack[-1] == self.number_in_bracket_stack[-1] \
                    and self.bracket_stack[-1] == current_number_of_bracket:
                self.number_in_bracket_stack.pop()
                while self.bracket_stack and self.bracket_stack[-1] \
                        == current_number_of_bracket:
                    new_list.append(')')
                    self.bracket_stack.pop()

    def _handle_left_chained_operators(self, left_chained_operator):
        """
        The function handle the left chained operator given to it by
        adding open bracket and zero before the operator and close
        bracket after at least one number and before operator
        with smaller or equal power
        :param left_chained_operator:the currently working on operator
        (as a char)
        """

        # initializing the new organized list
        new_list = []

        # initializing the current depth of brackets
        current_number_of_bracket = 0

        # initializing the stack that hold the bracket's depth that
        # needs to add closing bracket
        self.bracket_stack = []

        # initializing the stack that hold the bracket's depth of the
        # number was already found
        self.number_in_bracket_stack = []

        # scanning the previous organized list
        equation_list = self.organized_list
        for index_of_char in range(0, len(equation_list)):

            # saving current char
            current_char = equation_list[index_of_char]

            # if current_char is a number
            # add the number to the new organized list
            # and add that a number was found
            # in current_number_of_bracket (the adding is done
            # by using the number_in_bracket_stack)
            if isinstance(current_char, float):
                new_list.append(current_char)
                self._number_found_in_current_bracket(
                    current_number_of_bracket)

            # if current_char is open brackets
            # add +1 to current_number_of_bracket (depth in brackets)
            # and add that open brackets to the new organized list
            elif current_char == '(':
                current_number_of_bracket += 1
                new_list.append(current_char)

            # if current_char is close brackets
            # add close bracket if needed
            # add that a number was found in current_number_of_bracket-1
            # add that open bracket to the new organized list
            # and decrease the current_number_of_bracket by one(depth in
            # brackets)
            elif current_char == ')':
                self._handle_close_bracket_char(current_number_of_bracket,
                                                new_list)
                current_number_of_bracket -= 1

            # if got to here current char must be operator
            # call _handle_operator() to manage the operators
            else:
                self._handle_operator(left_chained_operator,
                                      current_char,
                                      index_of_char, new_list,
                                      current_number_of_bracket, equation_list)

        # after scanning all the equation add the remaining bracket to
        # the new organized list
        self._put_all_remaining_bracket_in_list(new_list)
        return new_list

    def _handle_right_chained_operators(self, right_chained_operator):
        """
        The Function handles the right chaining operator that was given
        to it, meaning adding zero to the right of the operator
        :param right_chained_operator: The right chaining operator
        currently working on
        :return:The new organized list
        """

        # initializing the new organized list
        new_list = []

        # scanning the previews organized list
        equation_list = self.organized_list
        for index_of_char in range(0, len(equation_list)):

            # saving the current char
            current_char = equation_list[index_of_char]

            new_list.append(current_char)

            # if the current char is the char working on
            # add after the operator a zero
            if right_chained_operator == current_char:
                new_list.append(0.0)
        return new_list
