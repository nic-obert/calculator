#include "definitions.h"
#include <stdio.h>


char* typeNames[] = {
    "NULL",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "POW",
    "NUM",
    "SQRT",
    "L_PAREN",
    "R_PAREN"
};


void printTokens(Token* tokens)
{
    for (; tokens->next != NULL; tokens=tokens->next)
        printf("<%s> %f (%d)\n", typeNames[tokens->type], tokens->value, tokens->priority);
}
