from convert_list_to_organized_list import ConvertListToOrganizedList
from infix_to_postfix_convertor import InfixToPostfixConvertor
from calculation_result import CalculationResult


class Model:
    def solve_equation(self, metadata):
        """
        This function solve the equation
        :param metadata:Hold information about the equation
        :return:CalculationResult(object) that hold whether or not the
        calculation was successful(if it was unsuccessful it will hold the
        error code) and the calculation result
        """

        # convert the equation from infix expression to postfix
        postfix_list = self._prepare_list_before_solve(metadata)

        # check if the equation is only one number
        # if true create CalculationResult is the number as the result
        # and return the CalculationResult
        if len(postfix_list) == 1:
            calculation_result = CalculationResult()
            calculation_result.result = postfix_list[0]
            return calculation_result
        # stack that hold the operands
        operands_stack = []

        # scanning all the equation
        for current_char in postfix_list:

            # if current char is number push to the stack
            if isinstance(current_char, float):
                operands_stack.append(current_char)

            # else current_char is operator
            else:

                # pop the last two numbers from the operands stack
                second_number = operands_stack.pop()
                first_number = operands_stack.pop()

                # calculate the expression by calling the calculate
                # function of the operator instance from the
                # OPERATORS_DICTIONARY
                calculation_result = metadata. \
                    OPERATORS_DICTIONARY[current_char] \
                    .calculate(first_number, second_number)

                # check if the calculation was successful
                # if true push the calculation result to operands stack
                # else return the calculation_result that hold the
                # calculation error
                if calculation_result.is_successful:
                    operands_stack.append(calculation_result.result)
                else:
                    return calculation_result
        return calculation_result


    def _prepare_list_before_solve(self, metadata):
        """
        This function organized the equation by adding zero and
        brackets at selected places(detailed explanation about the rules
        where to add what is found in the document given in github)
        and than covert the equation from
        infix to postfix equation
        :param metadata:Hold important information about the equation
        :return:The equation as postfix expression after being
        "organized"
        """

        # create the organized list convertor
        organized_list_convertor = ConvertListToOrganizedList(metadata)

        # convert the list to organized equation
        organized_list = organized_list_convertor.create_organize_list()

        # create the postfix convertor
        postfix_convertor = InfixToPostfixConvertor(organized_list,
                                                    metadata
                                                    .OPERATORS_DICTIONARY)

        # convert the equation to postfix
        return postfix_convertor.infix_to_postfix()
