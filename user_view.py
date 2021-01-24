from equation_status_code import InvalidEquationCode


class UserView:
    def __init__(self):
        """
        build the class that  responsible on the user
        UI(present massages and get input)
        """

        # dictionary that link all the invalid equation code to the
        # corresponding error massage
        self.ERROR_MASSAGE_DIC = {
            InvalidEquationCode.VALID: "Valid",
            InvalidEquationCode.UNDEFINED_CHARACTERS:
                "Undefined characters in your equation",
            InvalidEquationCode.CLOSE_WITHOUT_OPEN_BRACKET:
                "Close bracket without open one",
            InvalidEquationCode.EMPTY_EQUATION:
                "Empty equation",
            InvalidEquationCode.TOO_MANY_OPEN_BRACKET:
                "Too many open brackets...(missing close brackets)",
            InvalidEquationCode.OPERATORS_OPERANDS_ERROR:
                "Missing operators/operands..",
            InvalidEquationCode.TOO_MANY_DOTS:
                "Too many dots in one number",
            InvalidEquationCode.UNNECESSARY_BRACKET:
                "Unnecessary brackets in your equation",
            InvalidEquationCode.DIVISION_BY_ZERO:
                "Division by zero is undefined",
            InvalidEquationCode.FACTORIAL_ON_NEGATIVE_NUMBER:
                "Factorial on negative number is illegal",
            InvalidEquationCode.FACTORIAL_ON_DECIMAL_NUMBER:
                "Factorial on negative number is illegal",
            InvalidEquationCode.NUMBER_TOO_BIG: "Number is too big",
            InvalidEquationCode.COMPLEX_NUMBER: "Complex number",
            InvalidEquationCode.EMPTY_DECIMAL_POINT:
                "Empty decimal point....(missing number)",
        }

    def is_user_want_solve_equation(self):
        """
        Present the user with the program menu and get his decision on
        what to do next
        :return: User decision(True if user wants to solve an equation)
        """
        self._present_user_calculator_options_interface()
        return self._is_user_wants_to_continue()

    def _present_user_calculator_options_interface(self):
        """
        Present the user with the program menu
        """
        print("\nwelcome to the calculator")
        print("What would you like to do")
        print("Choose a number:")
        print("1)Solve an equation")
        print("2)Exit")

    def _is_user_wants_to_continue(self):
        """
        Get user decision whether to solve another equation (input==1)
        or quit (input==2)
        :return: User decision(True if the user wants to solve another
        equation False if not)
        """

        # dummy value to get in while
        user_input = -1
        while user_input != 1 and user_input != 2:

            try:
                # convert the string into int
                user_input = int(input())
            except ValueError:
                print("Please enter a number")
                continue
            except Exception as e:
                print("something went wrong please try again " + str(e))
                continue

            # check if the user_input was one of the options
            # if not present a error massage and try again
            if user_input != 1 and user_input != 2:
                print("Please enter a valid number(1-2)")
                continue

        return user_input == 1

    def get_equation_from_user(self):
        """
        Get a non empty string from user(the equation)
        :return:The string that was given from user
        """
        while True:
            try:
                # Get the string from the user
                string_equation = input("Please enter an valid equation")

                # If empty get new string
                while not string_equation:
                    string_equation = input(
                        "Please enter an valid not empty equation")
                break
            except Exception as e:
                print("something went wrong please try again " + str(e))

        return string_equation

    def present_error_massage(self, invalid_equation_code):
        """
        Present to user the error in the equation
        :param invalid_equation_code: the code of the error in the
         equation
        """
        print("Invalid equation")
        print(self.ERROR_MASSAGE_DIC[invalid_equation_code])

    def present_solved_equation(self, result):
        """
        Present to user the answer to his equation
        :param result: The answer to the equation that will be printed
        """
        print("the result to the equation is:", result)

    def present_exit_massage(self):
        """
        Present to user exit massage
        """
        print("Thank you for using the calculator....")
