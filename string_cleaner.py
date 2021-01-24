
def remove_white_spaces(equation_string, LEGAL_WHITE_SPACES):
    """
    The function return the string given without the legal white space
    :param equation_string: The string working on
    :param LEGAL_WHITE_SPACES: Set of all the legal white spaces
    :return: New string without legal white space
    """

    # for every white legal space in set
    for legal_white_space in LEGAL_WHITE_SPACES:
        # delete the white space
        equation_string = equation_string.replace(legal_white_space, '')

    return equation_string
