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

	**Controller**
Class that responsible on navigation between the different scenarios and stages of the solve.the controller does one step at a time (according to the status)
After a step is finish change the status to next step
If error was found change step to accordingly and start over again

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

	**ConvertListToOrganizedList**
class that responsible on converting the List to organized list. in order to handle the chaning and the one number operators.
the ConvertListToOrganizedList create a new list where before every chaining operator it adds "(0" and after the chaining is complate it add ")", in addition it add zero to every one number operator to one of its sides(depanding if its right of number or left to number operator).
for example the equation "4--(-5$7)+4!" will became 4-(0-(0-5$&))+4!0


	**Model**
Class that responsible on solving the equation after convrting it to postfix expression

	**All the test modules**
Those modules are used to test various class in many different scenarios,the class that are being tested are:StringValidator, StringToListConverter, remove_white_spaces(function), Model, InfixToPostfixConvertor, ConvertListToOrganizedLis


# the algoritm

after doing all the pre calculation test and passing them successfully the calculator solve the equation by first converting the equation to an OrganizedList and after that converting it to a postfix expression (from infix).
this way of solving the equation has made it possible to solve all the equation in a **Time complexity of O(n)

# Future development

In order to add a new operator to the calculator the develpoper needs to do 2 things.
first the programmer needs to create a class for that operator that inherit from the OperatorAbstract and then
initialize its functions and properties 
secondly add that class to the OPERATORS_DICTIONARY as value and the operator char as the key 
