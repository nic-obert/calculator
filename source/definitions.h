#pragma once

#include <stdlib.h>

// token types

#define ADD_T 1
#define SUB_T 2
#define MUL_T 3
#define DIV_T 4
#define POW_T 5
#define NUM_T 6
#define SQRT_T 7
#define L_PAREN_T 8
#define R_PAREN_T 9

// priorities

#define NUM_P 0
#define ADD_P 3
#define SUB_P 3
#define MUL_P 4
#define DIV_P 4
#define POW_P 5
#define SQRT_P 5
#define PAREN_P 9


typedef struct Token {
    double value;
    unsigned char type;
    unsigned int priority;
    struct Token* next;
    struct Token* prev;
} Token;


Token* appendToken(Token* last)
{
    Token* token = (Token*)malloc(sizeof(Token));
    last->next = token;
    token->prev = last;
    token->next = NULL;
}


void removeUnaryOperator(Token* token)
{   
    if (token->next == NULL)
        token->prev->next = NULL;

    else if (token->prev == NULL)
        token->next->prev = NULL;

    else {
        token->next->prev = token->prev;
        token->prev->next = token->next;
    }
        
    free(token);
}


void removeBinaryOperator(Token* token)
{
    if (token->next->next == NULL) {
        // set previous token's next to NULL
        token->prev->next = NULL;

    } else {
        // set previous token's next to next token's next token
        token->prev->next = token->next->next;
        // set next token's next's previous to previous token
        token->next->next->prev = token->prev;
    }
    // free pointers
    free(token->next);
    free(token);
}
