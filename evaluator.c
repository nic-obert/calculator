#include "definitions.h"


Token* getHighestPriority(Token* tokens)
{
    while (tokens->type != NULL_T)
        ++ tokens;
    
    return tokens;

}




void evaluate(Token* tokens)
{
    while (tokens->type != NULL_T)
    {
        Token* token = getHighestPriority(tokens);
        
        switch (token->type)
        {
        case ADD_T:
            break;

        case SUB_T:
            break;
        
        default:
            // TODO implement error
            break;
        }
    }
}