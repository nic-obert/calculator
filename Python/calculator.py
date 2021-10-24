#!/usr/bin/env python3
from typing import Any, Callable, Dict, List, Tuple, Union
from enum import Enum
import math


# Custom error that indicates an error in the mathematical expression.
# It's needed to differentiate between exceptions derived from bugs and the ones
# generated from invalid user input.
class InvalidExpressionError(Exception):
    pass


# Mimicing a C enum
class TokenType(Enum):
    
    NUMBER = 'NUMBER'
    NEGATIVE_NUMBER = 'NEGATIVE_NUMBER'
    SUM = 'SUM'
    SUBTRACTION = 'SUBTRACTION'
    MULTIPLICATION = 'MULTIPLICATION'
    DIVISION = 'DIVISION'
    POWER = 'POWER'
    OPEN_PARENTHESIS = 'OPEN_PARENTHESIS'
    CLOSE_PARENTHESIS = 'CLOSE_PARENTHESIS'
    FUNCTION = 'FUNCTION'


# Python dictionary that maps a TokenType to an integer priority value
priority_map: Dict[TokenType, int] = {
    TokenType.NUMBER: 0,
    TokenType.NEGATIVE_NUMBER: 0,
    TokenType.CLOSE_PARENTHESIS: 0,
    TokenType.SUM: 1,
    TokenType.SUBTRACTION: 1,
    TokenType.MULTIPLICATION: 2,
    TokenType.DIVISION: 2,
    TokenType.POWER: 3,
    TokenType.FUNCTION: 4,
    TokenType.OPEN_PARENTHESIS: 5
}


MAX_PRIORITY = priority_map[TokenType.OPEN_PARENTHESIS]


def get_token_type_priority(type: TokenType) -> int:
    return priority_map[type]


class Token:
    
    # Class initialization function, similar to other languages' constructor
    def __init__(self, type: TokenType, base_priority: int, value: Any = None) -> None:
        self.type = type

        self.priority = get_token_type_priority(self.type)
        # If the token type has priority 0 it shouldn't ever be executed, so don't add the base priority
        if (self.priority != 0):
            self.priority += base_priority

        self.value = value

    # Functions for printing the token in a neater way for debugging. They are not mandatory.
    def __repr__(self) -> str:
        return f'<{self.type}: {self.value} ({self.priority})>'
    
    def __str__(self) -> str:
        return self.__repr__()


# Type aliases used for type clarity
Number = Union[int, float]
# Function represents a mathematical function that takes a list of parameters as argument and returns a number.
Function = Callable[[List[Token]], Number]


# Square root mathematical functon
def sqrt(args: Tuple[Token]) -> Number:
    # Get the radicand from the argument list.
    radicand = args[0].value
    
    # Check if the radicand is negative and eventually throw an error.
    if radicand < 0:
        raise InvalidExpressionError(f'Invalid expression: radicand of root with even index cannot be negative')

    # Return the square root of the radicand
    return math.sqrt(radicand)


# N-index root mathematical function
def nroot(args: Tuple[Token, Token]) -> Number:
    # Get the radicand and root index from the argument list.
    radicand = args[0].value
    index = args[1].value

    # Check if the root index is even.
    if index % 2 == 0:
        # If so, check if the radicand is negative and eventually throw an error.
        if radicand < 0:
            raise InvalidExpressionError(f'Invalid expression: radicand of root with even index cannot be negative')

    # Return the index-root of the radicand.
    # The n-index root of a number a is defined as the number a raised to the 1/n power.
    # Note that in other languages you may need to use a floating point number instead (e.g. 1.0 instead of 1).
    return radicand ** (1 / index)


# Sine mathematical function
def sin(args: Tuple[Token]) -> Number:
    # Convert the angle in degrees to radians, since Python's math library uses radians.
    radians = math.radians(args[0].value)
    # Return the sine of the given number
    return math.sin(radians)


# Cosine mathematical function
def cos(args: Tuple[Token]) -> Number:
    # Convert the angle in degrees to radians, since Python's math library uses radians.
    radians = math.radians(args[0].value)
    # Return the cosine of the given number
    return math.cos(radians)


# Tangent mathematical function
def tan(args: Tuple[Token]) -> Number:
    # Convert the angle in degrees to radians, since Python's math library uses radians.
    radians = math.radians(args[0].value)
    # Return the tangent of the given number
    return math.tan(radians)


# The function map is a dictionary that maps a mathematical function name to its implementation.
function_map: Dict[str, Function] = \
{
    'sqrt': sqrt,
    'nroot': nroot,
    'sin': sin,
    'cos': cos,
    'tan': tan
}


def get_expression() -> str:
    while True:
        try:
            # Get the input from the terminal. Remove any whitespaces as they're not useful.
            expression = input('Enter your mathematical expression\n> ').replace(' ', '')
            # Add an "exit" command to terminate the script
            if expression == 'exit':
                exit(0)
            # Check if the input string isn't empty
            if len(expression) > 0:
                break
        
        except KeyboardInterrupt:
            # In case of Ctrl-C, ask again for input
            continue
        
        except EOFError:
            # If Ctrl-D is hit, terminate the script
            exit(0)
    
    return expression


# Utility function for lexical analysis
def is_function_name(char: str) -> bool:
    # Get the character's ASCII value with the Python built-in ord() function.
    ascii_value = ord(char)
    # Return True for ASCII values between A-Z and a-z.
    # For reference, take a look at the ASCII table.
    return 64 < ascii_value < 91 or 96 < ascii_value < 123


def tokenize_expression(expression: str) -> List[Token]:
    token_list: List[Token] = []
    # Current token that is being built.
    token: Union[Token, None] = None
    # Base token priority from parenthesis depth (0 is no depth).
    base_priority = 0

    # Iterate over every character in the string input.
    for char in expression:

        if token is not None:
            if token.type == TokenType.NUMBER:
                # If char is a digit, update the token's value.
                if char.isdigit():
                    # Formula for inserting a digit at the beginning of a positive number.
                    token.value = token.value * 10 + int(char)
                    continue
                # If char isn't a digit anymore, the numeric token has finished building.
                token_list.append(token)
                token = None
            
            elif token.type == TokenType.NEGATIVE_NUMBER:
                if char.isdigit():
                    # Formula for insertig a digit at the beginning of a negative number.
                    token.value = token.value * 10 - int(char)
                    continue
                # If value of negative number token is 0, it means that a standalone '-' operator was provided.
                # Consequently, throw an error because '-' alone doesn't have a meaning.
                if token.value == 0:
                    raise InvalidExpressionError(f'Invalid expression "{expression}": subtraction operator \'-\' not allowed in this context')
                token_list.append(token)
                token = None

            elif token.type == TokenType.FUNCTION:
                # Check whether the character can be part of a function name.
                if is_function_name(char):
                    # Update the function name.
                    token.value += char
                    continue
                # If char isn't a function name character anymore, the function name is complete.
                token_list.append(token)
                token = None
            
        # Check if the character is a digit.
        if char.isdigit():
            # Create a token that will be completed later.
            token = Token(TokenType.NUMBER, base_priority, int(char))
            continue
        
        # Check for arithmetical operators.
        if char == '+':
            token_list.append(Token(TokenType.SUM, base_priority))
            continue
        
        if char == '-':
            # If the previous token was a number or a close parenthesis, the '-' operator is a subtraction operator.
            if len(token_list) != 0 and (token_list[-1].type == TokenType.NUMBER or token_list[-1].type == TokenType.CLOSE_PARENTHESIS):
                token_list.append(Token(TokenType.SUBTRACTION, base_priority))
            else:
                # Whereas if the previous token wasn't a number, the '-' indicates a negatve number.
                token = Token(TokenType.NEGATIVE_NUMBER, base_priority, 0)
            continue
        
        if char == '*':
            token_list.append(Token(TokenType.MULTIPLICATION, base_priority))
            continue
        
        if char == '/':
            token_list.append(Token(TokenType.DIVISION, base_priority))
            continue
        
        if char == '^':
            token_list.append(Token(TokenType.POWER, base_priority))
            continue
        
        if char == '(':
            # Increase the base priority for operators inside parentheses.
            base_priority += MAX_PRIORITY
            token_list.append(Token(TokenType.OPEN_PARENTHESIS, base_priority))
            continue
        
        if char == ')':
            # Restore the previous base priority once exited from the parentheses.
            base_priority -= MAX_PRIORITY
            token_list.append(Token(TokenType.CLOSE_PARENTHESIS, base_priority))
            continue
        
        # The comma operator is used to divide numeric tokens, but it doesn't actually execute.
        if char == ',':
            continue
        
        # Check if char can be part of a function name.
        if is_function_name(char):
            token = Token(TokenType.FUNCTION, base_priority, char)
            continue
        
        # If char hasn't been handled yet, the expression contains an error.
        raise InvalidExpressionError(f"The expression {expression} contains an error: invalid character '{char}'")
    
    # Eventually, add the last token of the list, if it wasn't added before.
    if token is not None:
        token_list.append(token)

    return token_list


# Utility function that finds the token with the highest priority.
def get_highest_priority_token_index(token_list: List[Token]) -> int:
    # Variables to keep track of the current highest priority token.
    highest_priority_index = 0
    highest_priority = 0
    index = 0
    # Iterate over the token list to find the target token.
    for token in token_list:
        # If the next token has a bigger priority than the current one, keep track of it.
        if token.priority > highest_priority:
            highest_priority = token.priority
            highest_priority_index = index
        index += 1
    
    return highest_priority_index


# Utility function that returns the operands to the left and right of a binary operator.
def get_binary_operands(token_list: List[Token], index: int) -> Tuple[Token, Token]:
    return (
        token_list[index - 1],
        token_list[index + 1]
    )


# Utility function that removes the operands to the left and right of a binary operator
def remove_binary_operands(token_list: List[Token], index: int) -> None:
    # Pop the operands from the token list in reverse order so no to invalidate the indexes.
    token_list.pop(index + 1)
    token_list.pop(index - 1)


# Utility function that helps finding the correspondent closing parenthesis, given an open one.
def find_closing_parenthesis_index(token_list: List[Token], index: int) -> int:
    # Keep track of nested parentheses depth
    parenthesis_depth = 1
    # Perform the search only in a sublist of the token list, from (index + 1) to the end.
    for token in token_list[index + 1:]:
        index += 1
        if token.type == TokenType.OPEN_PARENTHESIS:
            # Update the depth in case of nested parentheses.   
            parenthesis_depth += 1
        elif token.type == TokenType.CLOSE_PARENTHESIS:
            # Restore the previus depth once the parenthesis is closed.
            parenthesis_depth -= 1
            # If the parenthesis depth is 0, the closing parenthesis has been found.
            if parenthesis_depth == 0:
                return index


def evaluate_expression(token_list: List[Token]) -> Number:
    # Evaluate while there are still operations to execute.
    while True:
        # Get the next operator token to evaluate.
        token_index = get_highest_priority_token_index(token_list)
        token = token_list[token_index]
        
        # If the highest priority token has priority 0, there are no more tokens to evaluate.
        if token.priority == 0:
            return token.value
        
        # Set the token's priority to 0 so not to evaluate it twice
        token.priority = 0

        # Handle every operator differently, based on its operation
        if token.type == TokenType.SUM:
            # Get the left and right operands of the binary operator '+'
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            # Calculate the result of the addition between the two operands.
            result = left_operand.value + right_operand.value
            # Change the token't type to NUMBER in order to use it to store the operation's result.
            token.type = TokenType.NUMBER
            # Store the operation's result
            token.value = result
            # Remove the just-used operands from the token list.
            remove_binary_operands(token_list, token_index)

        elif token.type == TokenType.SUBTRACTION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value - right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.MULTIPLICATION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value * right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.DIVISION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            # Check if the divisor is 0. Consequently, throw an error indicating a mistake in the expression.
            if right_operand.value == 0:
                raise InvalidExpressionError('Invalid expression: cannot divide by zero')
            
            result = left_operand.value / right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.POWER:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            # For anyone wondering, ** is the power operator in Python.
            result = left_operand.value ** right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.OPEN_PARENTHESIS:
            # Find the position of the corresponding closing parenthesis.
            closing_parenthesis_index = find_closing_parenthesis_index(token_list, token_index)

            # Differentiate between function calls and plain parentheses:
            # if the previous token is a function, this parenthesis is supposed to contain its arguments.
            if token_list[token_index - 1].type == TokenType.FUNCTION:
                # The parenthesis token's value is set to a list containing the function call arguments.
                token.value = []
                # Move the tokens inside the parentheses inside the argument list.
                for children in token_list[token_index + 1 : closing_parenthesis_index]:
                    token.value.append(children)
                # Remove the unneded tokens from the token list.
                # Perform a reverse iteration over token_list so not to invalidate any list index during element removal.
                for index in range(closing_parenthesis_index, token_index, -1):
                    token_list.pop(index)
            
            # If the previous token isn't a function, this pair of parentheses are just normal parentheses.
            else:
                # Evaluate nothing, since these the priority of their content has already been updated during tokenization.
                # Pop the parentheses in reverse order.
                token_list.pop(closing_parenthesis_index)
                token_list.pop(token_index)
        
        elif token.type == TokenType.FUNCTION:
            # Get the parenthesis token from the token list.
            parenthesis = token_list[token_index + 1]
            # Search the function map (dictionary) for the called function.
            function = function_map.get(token.value)
            # If the function isn't defined, throw an error.
            if function is None:
                raise InvalidExpressionError(f'Invalid expression: undefined function "{token.value}"')
            # Call the mathematical function.
            # The parenthesis' value is the list of argument tokens to pass to the function.
            token.value = function(parenthesis.value)

            token.type = TokenType.NUMBER
            token_list.pop(token_index + 1)


def print_token_list(token_list: List[Token]) -> None:
    for token in token_list:
        print(token)


def main() -> None:
    # Run the calculator indefinitely
    while True:
        try:
            # Get the mathematical expression input string from the user
            expression = get_expression()
            # Tokenize the input string
            token_list = tokenize_expression(expression)
            # print_token_list(token_list)
            # Calculate the expression's result
            result = evaluate_expression(token_list)
            # Finally print the result
            print(f'The result is {result}')
        
        except KeyboardInterrupt:
            # Terminate the loop when Ctrl-C is hit
            break
        
        except InvalidExpressionError as exc:
            # In case of an invalid mathematical expression, print what's the problem
            print(exc)
            continue    
        

# Run the main function only if the script was run directly
if __name__ == '__main__':
    main()

