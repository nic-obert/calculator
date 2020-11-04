#include <stdlib.h>
#include <string.h>

#include "definitions.h"

#define isNumber(x) (47 < x && x < 58)
#define isLetter(x) (96 < x && x < 123)
#define compare(x, y) (strcmp(x, (const char*)y))


Token* parse(const char* expr)
{   
    // Token* tokens should be a linked list
    Token* tokens = (Token*)malloc(sizeof(Token));
    // current token
    Token* token = tokens;
    token->prev = NULL;

    for (; *expr != '\0'; ++expr)
    {

        switch (*expr)
        {
        // switch for single-character operators
        
        case '+':
            token->type = ADD_T;
            token->priority = ADD_P;
            break;
        case '-':
            token->type = SUB_T;
            token->priority = SUB_P;
            break;
        case '*':
            token->type = MUL_T;
            token->priority = MUL_P;
            break;
        case '/':
            token->type = DIV_T;
            token->priority = DIV_P;
            break;
        case '^':
            token->type = POW_T;
            token->priority = POW_P;
            break;
        case '(':
            token->type = L_PAREN_T;
            token->priority = PAREN_P;
            break;
        case ')':
            token->type = R_PAREN_T;
            token->priority = PAREN_P;
            break;


        // for operators longer than 1 character / numbers

        default:

            if (isNumber(*expr))
            {
                token->type = NUM_T;
                token->priority = NUM_P;
                token->value = *expr - 48; // ASCII 0 is 48
                expr ++;

                // check if character is part of a bigger number
                for (; isNumber(*expr); ++expr)
                {
                    token->value = token->value * 10 + *expr - 48;
                }
                expr --;
            }

            else if (isLetter(*expr))
            {
                // create a zero-initialized buffer for lettrs of function name to be stored
                char letterBuffer[9] = {0,0,0,0,0,0,0,0,0};
                unsigned char letterBufferIndex = 0;
                letterBuffer[letterBufferIndex] = *expr;
                expr ++;

                // as long as current character is a letter --> build the function name
                for (; isLetter(*expr); ++expr)
                {
                    letterBuffer[letterBufferIndex] = *expr;
                    letterBufferIndex ++;
                }
                // reduce index
                expr --;

                if (compare("sqrt", letterBuffer))
                {
                    token->type = SQRT_T;
                    token->priority = SQRT_P;
                }
                
                // TODO implement error handling in case function name is not defined
            }

            break;


        } // end of switch statement
        
        // add a token to the linked list
        token->next = (Token*)malloc(sizeof(Token));
        token->next->prev = token;
        token = token->next;
        
    } // end of for loop

    // the end of the linked list
    token->next = NULL;

    // return the heap-allocated tokenized array
    return tokens;
}

