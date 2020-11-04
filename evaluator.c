#include "definitions.h"

#include <stdlib.h>
#include <math.h>


Token* getHighestPriority(Token* tokens)
{   
    Token* highest = tokens;
    for (; tokens != NULL; tokens=tokens->next  )
    {
        if (tokens->priority > highest->priority)
            highest = tokens;
    }
    
    if (highest->priority != 0)
        return highest;
    return NULL;
}


void evaluate(Token* tokens)
{
    while (1)
    {   
        Token* token = getHighestPriority(tokens);
        if (token == NULL)
            break;
        
        switch (token->type)
        {
        case ADD_T:
            // update value
            token->prev->value += token->next->value;
            // remove redundant tokens from linked list
            token->next->next->prev = token->prev; // set next token's prev to the resulting token
            token->prev->next = token->next->next; // set previous token's next to the next token
            // free the pointers to avoid memory leaks
            free(token->next);
            free(token);
            break;

        case SUB_T:
            token->prev->value -= token->next->value;
            token->next->next->prev = token->prev;
            token->prev->next = token->next->next;
            free(token->next);
            free(token);
            break;
        
        case MUL_T:
            token->prev->value *= token->next->value;
            token->next->next->prev = token->prev;
            token->prev->next = token->next->next;
            free(token->next);
            free(token);
            break;
        
        case DIV_T:
            token->prev->value /= token->next->value;
            token->next->next->prev = token->prev;
            token->prev->next = token->next->next;
            free(token->next);
            free(token);
            break;
        
        case POW_T:
            token->prev->value = pow(token->prev->value, token->next->value);
            token->next->next->prev = token->prev;
            token->prev->next = token->next->next;
            free(token->next);
            free(token);
            break;
        
        default:
            // TODO implement error
            printf("Token evaluation error");
            break;
        }
    }
}