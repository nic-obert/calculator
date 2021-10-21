#!/usr/bin/env python3
# Allows classes to reference themselves
from __future__ import annotations
from typing import Any, Dict, List, Tuple, Union
from enum import Enum


# Mimicing a C enum
class TokenType(Enum):
    
    NUMBER = 'NUMBER'
    SUM = 'SUM'
    SUBTRACTION = 'SUBTRACTION'
    MULTIPLICATION = 'MULTIPLICATION'
    DIVISION = 'DIVISION'
    POWER = 'POWER'
    OPEN_PARENTHESIS = 'OPEN_PARENTHESIS'
    CLOSE_PARENTHESIS = 'CLOSE_PARENTHESIS'
    FUNCTION = 'FUNCTION'

priority_map: Dict[TokenType, int] = {
    TokenType.NUMBER: 0,
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
    
    def __init__(self, type: TokenType, base_priority: int, value: Any = None) -> None:
        self.type = type
        self.priority = base_priority + get_token_type_priority(self.type)
        self.value = value


def get_expression() -> str:
    while True:
        try:
            expression = input('Enter your mathematical expression\n> ').strip()
            if expression == 'exit':
                exit(0)
            if len(expression) > 0:
                break
        except KeyboardInterrupt:
            continue
        except EOFError:
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
            token_list.append(Token(TokenType.SUBTRACTION, base_priority))
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
            token_list.append(Token(TokenType.OPEN_PARENTHESIS, base_priority))
            base_priority += TokenType.MAX_PRIORITY
            continue
        if char == ')':
            token_list.append(Token(TokenType.CLOSE_PARENTHESIS, base_priority))
            base_priority -= TokenType.MAX_PRIORITY
            continue
        
        if is_function_name(char):
            token = Token(TokenType.FUNCTION, base_priority, char)
            continue
        
            
        raise ValueError(f"The expression {expression} contains an error: invalid character '{char}'")
    
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
    index = 0
    for token in token_list[index + 1:]:
        if token.type == TokenType.OPEN_PARENTHESIS:
            parenthesis_depth += 1
        elif token.type == TokenType.CLOSE_PARENTHESIS:
            parenthesis_depth -= 1
            if parenthesis_depth == 0:
                return index
        index += 1


def evaluate_expression(token_list: List[Token]) -> Union[float, int]:
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
            token.value = token.value = result
            remove_binary_operands(token_list, token_index)

        elif token.type == TokenType.SUBTRACTION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value - right_operand.value
            token.type = TokenType.NUMBER
            token.value = token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.MULTIPLICATION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value * right_operand.value
            token.type = TokenType.NUMBER
            token.value = token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.DIVISION:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            if right_operand.value == 0:
                raise ZeroDivisionError('Invalid expression: cannot divide by zero')
            result = left_operand.value / right_operand.value
            token.type = TokenType.NUMBER
            token.value = token.value = result
            remove_binary_operands(token_list, token_index)
        
        elif token.type == TokenType.POWER:
            left_operand, right_operand = get_binary_operands(token_list, token_index)
            result = left_operand.value ** right_operand.value
            token.type = TokenType.NUMBER
            token.value = token.value = result
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
            # TODO define a function dictionary
            pass


def print_token_list(token_list: List[Token]) -> None:
    for token in token_list:
        print(f'<{token.type}: {token.value} ({token.priority})>')


def main() -> None:
    while True:
        try:
            expression = get_expression()
            token_list = tokenize_expression(expression)
            print_token_list(token_list)
            result = evaluate_expression(token_list)
            print(f'The result is {result}')
        except KeyboardInterrupt:
            break
        except Exception as exc:
            print(exc)
            continue    
        

if __name__ == '__main__':
    main()

