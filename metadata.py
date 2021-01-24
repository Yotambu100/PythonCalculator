class MetaData(object):
    def __init__(self, OPERATORS_DICTIONARY):

        # The equation from the user as a string
        self.equation_string = None

        # The equation as a list
        self.equation_list = None

        # enum that hold an error code (if there is an error)
        self.invalid_equation_error_code = None

        # an instance of class that hold the result of the calculation,
        # if the calculation was successful and error code if the calculation
        # failed
        self.calculation_result = None

        # dictionary that link all the operators char as key and
        # their respectively operator class instance as value
        self.OPERATORS_DICTIONARY = OPERATORS_DICTIONARY
