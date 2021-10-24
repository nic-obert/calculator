#!/usr/bin/env python3
from typing import Any, Callable, Dict, List, Tuple, Union
from enum import Enum
import math


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


Number = Union[int, float]
Function = Callable[[List[Token]], Number]


def sqrt(args: Tuple[Token]) -> Number:
    radicand = args[0].value
    
    # Check if the root index is even.
    # If so, check if the radicand is negative and eventually throw an error.
    if radicand < 0:
        raise InvalidExpressionError(f'Invalid expression: radicand of root with even index cannot be negative')

    return math.sqrt(radicand)


def nroot(args: Tuple[Token, Token]) -> Number:
    radicand = args[0].value
    index = args[1].value

    # Check if the root index is even.
    # If so, check if the radicand is negative and eventually throw an error.
    if index % 2 == 0:
        if radicand < 0:
            raise InvalidExpressionError(f'Invalid expression: radicand of root with even index cannot be negative')

    # Return the index-root of the radicand.
    return radicand ** (1.0 / index)


def sin(args: Tuple[Token]) -> Number:
    radians = math.radians(args[0].value)
    return math.sin(radians)


def cos(args: Tuple[Token]) -> Number:
    radians = math.radians(args[0].value)
    return math.cos(radians)


def tan(args: Tuple[Token]) -> Number:
    radians = math.radians(args[0].value)
    return math.tan(radians)


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


def is_function_name(char: str) -> bool:
    ascii_value = ord(char)
    # Return True for characters A-Z and a-z
    return 64 < ascii_value < 91 or 96 < ascii_value < 123


def tokenize_expression(expression: str) -> List[Token]:
    token_list: List[Token] = []
    token: Union[Token, None] = None
    base_priority = 0

    for char in expression:

        if token is not None:
            if token.type == TokenType.NUMBER:
                if char.isdigit():
                    token.value *= 10
                    token.value += int(char)
                    continue
                # if char isn't a digit anymore, the numeric token is finished
                token_list.append(token)
                token = None
            
            elif token.type == TokenType.NEGATIVE_NUMBER:
                if char.isdigit():
                    token.value *= 10
                    token.value -= int(char)
                    continue
                # If value of negative number token is 0, it means that a standalone '-' was provided.
                # Consequently, throw an error.
                if token.value == 0:
                    raise InvalidExpressionError(f'Invalid expression "{expression}": subtraction operator \'-\' not allowed in this context')
                token_list.append(token)
                token = None

            elif token.type == TokenType.FUNCTION:
                if is_function_name(char):
                    token.value += char
                    continue
                # if char isn't a function name character anuìymore, the function name is finished
                token_list.append(token)
                token = None
            

        if char.isdigit():
            token = Token(TokenType.NUMBER, base_priority, int(char))
            continue
            
        if char == '+':
            token_list.append(Token(TokenType.SUM, base_priority))
            continue
        if char == '-':
            if len(token_list) != 0 and token_list[-1].type == TokenType.NUMBER:
                token_list.append(Token(TokenType.SUBTRACTION, base_priority))
            else:
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
            base_priority += MAX_PRIORITY
            token_list.append(Token(TokenType.OPEN_PARENTHESIS, base_priority))
            continue
        if char == ')':
            base_priority -= MAX_PRIORITY
            token_list.append(Token(TokenType.CLOSE_PARENTHESIS, base_priority))
            continue
        if char == ',':
            continue
        
        if is_function_name(char):
            token = Token(TokenType.FUNCTION, base_priority, char)
            continue
        
            
        raise InvalidExpressionError(f"The expression {expression} contains an error: invalid character '{char}'")
    
    # Eventually, add the last token of the list, if it wasn't added before
    if token is not None:
        token_list.append(token)

    return token_list


def get_highest_priority_token_index(token_list: List[Token]) -> int:
    highest_priority_index = 0
    highest_priority = 0
    index = 0
    for token in token_list:
        if token.priority > highest_priority:
            highest_priority = token.priority
            highest_priority_index = index
        index += 1
    return highest_priority_index


def get_binary_operands(token_list: List[Token], index: int) -> Tuple[Token, Token]:
    return (
        token_list[index - 1],
        token_list[index + 1]
    )


def remove_binary_operands(token_list: List[Token], index: int) -> None:
    # pop the operands from the token list in reverse order so no to invalidate the indexes
    token_list.pop(index + 1)
    token_list.pop(index - 1)


def find_closing_parenthesis_index(token_list: List[Token], index: int) -> int:
    parenthesis_depth = 1
    for token in token_list[index + 1:]:
        index += 1
        if token.type == TokenType.OPEN_PARENTHESIS:
            parenthesis_depth += 1
        elif token.type == TokenType.CLOSE_PARENTHESIS:
            parenthesis_depth -= 1
            if parenthesis_depth == 0:
                return index


def evaluate_expression(token_list: List[Token]) -> Number:
    while True:
        token_index = get_highest_priority_token_index(token_list)
        token = token_list[token_index]
        # if the highest token has priority 0, there are no more tokens to evaluate
        if token.priority == 0:
            return token.value
        # set the token's priority to 0 so not to evaluate it twice
        token.priority = 0

        if token.type == TokenType.SUM:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value + right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
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
            if right_operand.value == 0:
                raise InvalidExpressionError('Invalid expression: cannot divide by zero')
            result = left_operand.value / right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.POWER:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value ** right_operand.value
            token.type = TokenType.NUMBER
            token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.OPEN_PARENTHESIS:
            closing_parenthesis_index = find_closing_parenthesis_index(token_list, token_index)

            if token_list[token_index - 1].type == TokenType.FUNCTION:
                token.value = []
                # Move the tokens inside the parentheses inside an internal list
                for children in token_list[token_index + 1 : closing_parenthesis_index]:
                    token.value.append(children)
                # Remove the unneded tokens from the token list
                # Perform a reverse iteration over token_list so not to invalidate any list index during element popping
                for index in range(closing_parenthesis_index, token_index, -1):
                    token_list.pop(index)
            else:
                # Evaluate nothing, just pop the parentheses in reverse order
                token_list.pop(closing_parenthesis_index)
                token_list.pop(token_index)
        
        elif token.type == TokenType.FUNCTION:
            parenthesis = token_list[token_index + 1]
            function = function_map.get(token.value)
            if function is None:
                raise InvalidExpressionError(f'Invalid expression: undefined function "{token.value}"')
            # parenthesis' value is the list of argument tokens
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

