import enum

from string_to_list_converter import StringToListConverter
from string_cleaner import *
from metadata import MetaData
from model import Model
from string_validator import StringValidator
from user_view import UserView
from operators import *


# enum of calculation status
class Status(enum.Enum):
    STARTING = 1
    GETTING_EQUATION = 2
    VALID_CHECK = 3
    INVALID_EQUATION = 4
    SOLVE_EQUATION = 5
    FINISH = 6
    EXIT = 7


class Controller:
    def __init__(self):

        # controller status determine what step the control should be doing
        self.controller_status = Status.STARTING

        # model responsible on the calculation
        self.model = Model()

        # user_view responsible on the user ui and input
        self.user_view = UserView()

        # metadata hold important information about the equation
        self.metadata = None

        # dictionary that link all the operators char as key and
        # their respectively operator class instance as value
        self.OPERATORS_DICTIONARY = {
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

        # Contain all the white space legal in string
        self.LEGAL_WHITE_SPACES = {' ', '\t', '\n'}

    def run(self):
        """
        Main Function.
        the function does one step at a time (according to the status)
        After a step is finish change the status to next step
        If error was found change step to accordingly and start over again
        """

        # the controller run until the user wants to stop (EXIT)
        while self.controller_status != Status.EXIT:

            # status == STARTING (at the start of the solver)
            # create metadata of the equation
            # determine if the user want to solve equation or exit
            if self.controller_status == Status.STARTING:

                # create metadata for new equation
                self.metadata = MetaData(self.OPERATORS_DICTIONARY)

                # check if user wants to solve equation
                if self.user_view.is_user_want_solve_equation():

                    # If true Need to get an equation from user
                    self.controller_status = Status.GETTING_EQUATION
                else:

                    # If false Game status == FINISH
                    self.controller_status = Status.FINISH

            # status == GETTING_EQUATION
            # Get the equation from user
            elif self.controller_status == Status.GETTING_EQUATION:
                self.metadata.equation_string = \
                    self.user_view.get_equation_from_user()

                # Remove all the white spaces in equation
                self.metadata.equation_string = remove_white_spaces(
                    self.metadata.equation_string,
                    self.LEGAL_WHITE_SPACES)

                # After the equation is received need to check validation
                self.controller_status = Status.VALID_CHECK

            # status == VALID_CHECK
            # check if the equation valid (before calculation)
            elif self.controller_status == Status.VALID_CHECK:

                # create the validator object
                string_validator = StringValidator(self.metadata)

                # if valid convert the equation to list and
                # continue to solve equation
                # if not move to INVALID_EQUATION
                if string_validator.is_equation_valid():
                    convertor = StringToListConverter()
                    self.metadata.equation_list = convertor \
                        .convert_string_to_list(self.metadata.equation_string)
                    self.controller_status = Status.SOLVE_EQUATION
                else:
                    self.controller_status = Status.INVALID_EQUATION

            # status == INVALID_EQUATION
            # present appropriate error massage
            # (according to the invalid reason)
            elif self.controller_status == Status.INVALID_EQUATION:
                self.user_view.present_error_massage(
                    self.metadata.invalid_equation_error_code)
                self.controller_status = Status.STARTING

            # status == SOLVE_EQUATION
            # try solving the equation, if successful present answer and
            # start again(status = STARTING )
            # if not successful present user error massage
            # accordingly (status = INVALID_EQUATION)
            elif self.controller_status == Status.SOLVE_EQUATION:
                self.metadata.calculation_result = self.model.solve_equation(
                    self.metadata)

                # check if calculation was successful
                if self.metadata.calculation_result.is_successful:
                    self.user_view.present_solved_equation(
                        self.metadata.calculation_result.result)
                    self.controller_status = Status.STARTING
                else:
                    self.metadata.invalid_equation_error_code = \
                        self.metadata.calculation_result.invalid_equation_code
                    self.controller_status = Status.INVALID_EQUATION

            # status == FINISH
            # present exit massage and exit function (status = Status.EXIT)
            elif self.controller_status == Status.FINISH:
                self.user_view.present_exit_massage()
                self.controller_status = Status.EXIT
