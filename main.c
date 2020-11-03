#include <stdio.h>

#include "evaluator.c"
#include "parser.c"
#include "utils.c"

int main(int argc, char const *argv[])
{   

    
    if (argc != 2) {
        printf("Exactly 1 argument is required, but %d were given\n", argc-1);
        exit(1);
    }
    

    // heap-allocated array --> to free
    Token* tokens = parse(argv[1]);
    

    printTokens(tokens);

    free(tokens);
    
    return 0;
}
