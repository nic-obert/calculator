#pragma once

// token types

#define NULL_T 0
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
#define PAREN_P 10


typedef struct {
    double value;
    unsigned char type;
    unsigned int priority;
} Token;

