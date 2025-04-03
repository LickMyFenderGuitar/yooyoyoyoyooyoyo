#ifndef FLUX_LEXER_H
#define FLUX_LEXER_H

#include <vector>
#include <string>

class Lexer {
public:
    static std::vector<std::string> tokenize(const std::string& code);
};

#endif // FLUX_LEXER_H
