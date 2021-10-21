#include "definitions.h"

#include <stdlib.h>
#include <math.h>


Token* getHighestPriority(Token* tokens)
{   
    Token* highest = tokens;
    for (; tokens != NULL; tokens=tokens->next)
    {
        if (tokens->priority > highest->priority)
            highest = tokens;
    }
    
    if (highest->priority != 0)
        return highest;
    return NULL;
}


Token* evaluate(Token* tokens)
{
    while (1)
    {   
        Token* token = getHighestPriority(tokens);
        if (token == NULL)
            break;
        
        switch (token->type)
        {
        case ADD_T:
            token->prev->value += token->next->value;
            removeBinaryOperator(token);
            break;

        case SUB_T:
            token->prev->value -= token->next->value;
            removeBinaryOperator(token);
            break;
        
        case MUL_T:
            token->prev->value *= token->next->value;
            removeBinaryOperator(token);
            break;
        
        case DIV_T:
            token->prev->value /= token->next->value;
            removeBinaryOperator(token);
            break;
        
        case POW_T:
            token->prev->value = pow(token->prev->value, token->next->value);
            removeBinaryOperator(token);
            break;
        
        case L_PAREN_T: ; // this semicolon has to be here
            // search for closing parenthesis while updating priorities
            Token* tok = token->next;
            unsigned char parenCount = 1;
            while (1)
            {
                if (tok->type == L_PAREN_T)
                    parenCount ++;
                else if (tok->type == R_PAREN_T)
                {
                    parenCount --;
                    if (parenCount == 0)
                        break;
                }
                
                if (tok->type != NUM_T)
                    tok->priority += PAREN_P;
                tok = tok->next;
            }

            // to prevent from freeing the array
            if (token->prev == NULL)
                tokens = token->next;

            // remove opening parenthesis
            removeUnaryOperator(token);
            // remove closing parenthesis
            removeUnaryOperator(tok);

            break;
        
        default:
            printf("Evaluation error occurred\n");
            printf("Token was: %uc %f\n", token->type, token->value);
            exit(EXIT_FAILURE);

        }
    }

    tokens->next = NULL;
    return tokens;
}