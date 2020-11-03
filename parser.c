#include <stdlib.h>
#include <string.h>

#include "definitions.h"

#define isNumber(x) (47 < x && x < 58)
#define isLetter(x) (96 < x && x < 123)
#define compare(x, y) (strcmp(x, (const char*)y))


Token* parse(const char* expr)
{   
    size_t length = strlen(expr);
    // Token* tokens should be a null-token-terminated array
    Token* tokens = (Token*)malloc(sizeof(Token) * (length + 1)); // +1 to avoid buffer overflows
    // current token
    Token* token = tokens;


    for (unsigned int i = 0; i != length; i++)
    {


        switch (expr[i])
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

            if (isNumber(expr[i]))
            {
                token->type = NUM_T;
                token->priority = NUM_P;
                token->value = expr[i] - 48; // ASCII 0 is 48
                i ++;

                // check if character is part of a bigger number
                for (; isNumber(expr[i]); i++)
                {
                    token->value = token->value * 10 + expr[i] - 48;
                }
                i --;
            }

            else if (isLetter(expr[i]))
            {
                // create a zero-initialized buffer for lettrs of function name to be stored
                char letterBuffer[9] = {0,0,0,0,0,0,0,0,0};
                unsigned char letterBufferIndex = 0;
                letterBuffer[letterBufferIndex] = expr[i];
                i ++;

                // as long as current character is a letter --> build the function name
                for (; isLetter(expr[i]); i++)
                {
                    letterBuffer[letterBufferIndex] = expr[i];
                    letterBufferIndex ++;
                }
                // reduce index
                i --;

                if (compare("sqrt", letterBuffer))
                {
                    token->type = SQRT_T;
                    token->priority = SQRT_P;
                }
                
                // TODO implement error handling in case function name is not defined
            }

            break;


        } // end of switch statement
        
        // increment token index
        ++ token;

        
    } // end of for loop

    // append a null-Token to the null-Token-terminated Token* tokens array
    token->type = NULL_T;

    // return the heap-allocated tokenized array
    return tokens;
}

