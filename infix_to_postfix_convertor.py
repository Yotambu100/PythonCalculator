class InfixToPostfixConvertor:
    """
    class that responsible on converting the equation to
    postfix equation(operator coming after two numbers)
    """

    def __init__(self, equation_list, OPERATORS_DICTIONARY):
        """
        build the class that responsible on converting the equation_list
        to postfix_list
        :param equation_list:The list working on
        :param OPERATORS_DICTIONARY:Dictionary that link all the
        operators char as key and their respectively operator class
        instance as value
        """
        self.equation_list = equation_list
        self.OPERATORS_DICTIONARY = OPERATORS_DICTIONARY

        # The new postfix list that will be make
        self.postfix_list = []

        # list (that function as a stack) that help converting the equation to
        # postfix equation
        self.operators_stack = []

    def infix_to_postfix(self):
        """
        This function create new postfix equation (as list) from the
        infix equation given at the constructor
        :return:The new postfix equation
        """

        # scanning all the equation
        for current_char in self.equation_list:

            # if current_char is number add to new postfix equation
            if isinstance(current_char, float):
                self.postfix_list.append(current_char)

            # if current_char is open bracket add to new postfix
            # equation
            elif current_char == '(':
                self.operators_stack.append(current_char)

            # if current_char is close bracket pop all of the operators
            # from the operators_stack until an open bracket is found
            # (and pop it too)
            elif current_char == ')':
                self._pop_all_operators_until_open_bracket()

            # if get to here current_char must be operator
            # if current operator power is bigger than the power of
            # the top operator at the stack push current operator
            # else pop all the element from operators_stack to
            # the postfix_list until the current operator power is
            # bigger than the power of the top operator at the
            # stack and than push current operator into the stack
            else:
                self.manage_operators_postfix(current_char)

        # after scanned all the equation if there are operators
        # left at the operators_stack pop them all to the new
        # postfix_list
        self._pop_all_remaining_operators()

        return self.postfix_list

    def _pop_all_operators_until_open_bracket(self):
        """
        This function pop all the operators from the operators_stack and
        put them in the new postfix_list until an open bracket is at
        the top of the stack(and than it pop the open bracket but
        doesnt add it to the new postfix_list)
        """

        # until the top of the stack is open bracket
        while self.operators_stack[-1] != '(':
            # pop from the stack and put in the new postfix_list
            self.postfix_list.append(self.operators_stack.pop())

        # pop the open bracket itself
        self.operators_stack.pop()

    def manage_operators_postfix(self, current_operator):
        """
        This function determine what to do when new operator is reached:
        if current operator power is bigger than the power of
        the top operator at the stack(or stack empty/top is open
        bracket) push current operator into stack
        else pop all the element from operators_stack to
        the postfix_list until the current operator power is
        bigger than the power of the top operator at the
        stack(or stack is empty/top is open bracket) and than push
        current operator to stack
        :param current_operator:The operator that was reached
        """

        # the power of the operator working on
        current_operator_power = self.OPERATORS_DICTIONARY[current_operator] \
            .operator_power

        # if the stack is empty or the stack top is open bracket
        # push operator to stack and return to main function
        if not self.operators_stack or self.operators_stack[-1] == '(':
            self.operators_stack.append(current_operator)
            return

        # the power of the operator at the top of the stack
        top_stack_operator_power = self.OPERATORS_DICTIONARY[
            self.operators_stack[-1]].operator_power

        # if current operator power is bigger than the power of
        # the top operator of the operators stack push current
        # operator into stack
        if current_operator_power > top_stack_operator_power:
            self.operators_stack.append(current_operator)
            return
        else:
            # else pop all the element from operators_stack to
            # the postfix_list until the current operator power is
            # bigger than the power of the top operator at the
            # stack(or stack is empty/top is open bracket) and than push
            # current operator to stack
            while self.operators_stack and self.operators_stack[-1] != '(' \
                    and self.OPERATORS_DICTIONARY[self.operators_stack[-1]] \
                    .operator_power >= current_operator_power:
                self.postfix_list.append(self.operators_stack.pop())
            self.operators_stack.append(current_operator)
            return

    def _pop_all_remaining_operators(self):
        """
        This function pop all the operators left at the operators_stack
        into the new postfix_list
        """

        # until the stack is empty
        while self.operators_stack:
            # pop stack into new postfix_list
            self.postfix_list.append(self.operators_stack.pop())
