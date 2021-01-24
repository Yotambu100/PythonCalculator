class CalculationResult:
    def __init__(self, is_successful=True, invalid_equation_code=None):

        # boolean that represent if the calculation was valid
        # default is True (most of the time calculation is valid)
        self.is_successful = is_successful

        # the result of the calculation
        self.result = None

        # enum that represent the error code if the calculation was invalid
        self.invalid_equation_code = invalid_equation_code
