# PythonCalculator

Made  by yotam buhnik

The calculator written in python 3.6 and tested with pytest 6.2.1

## User guide:

after running the program you will be presented with an welcome interface there you will have two options solve an equation(press 1) or exit the program(press 2)
if you prees one you will be asked to enter an equation, after you enterd it the calculator will solve the equation(if the equation was solvable) present the answer
and send you back to the welcome interface.
if you press two the progrem will stop.

## Developer guide:

# important modules and class

	**StringValidator**
Class that responsible on doing the pre validation of the equation.
the class preform several tests the equation as string and as list(different tests) to find error in the equation before sending it to the solver.
Error that the StringValidator can find are:undefined characters ,close without open bracket, empty_equation , too_many_open_bracket , operators_operands_error,
too_many_dots ,  unnecessary_bracket.

	**OperatorAbstract** 
Abstract class that everty operator inherit from and bind those operators to initialize functions and properties like: calculate, is_operator_two_number_operator,
operator_power, operator_position, is_chaining and is_operator_valid_at_index


	**InfixToPostfixConvertor**
class that responsible on converting the equation to postfix equation from infix

	gggg

	**Model**
Class that responsible on solving the equation after convrting it to postfix expression



# the algoritm

the calculator solve the equation

