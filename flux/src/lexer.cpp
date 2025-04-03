#include "lexer.h"
#include <cctype>
#include <iostream>

std::vector<std::string> Lexer::tokenize(const std::string& code) {
    std::vector<std::string> tokens;
    std::string token;
    for (char c : code) {
        if (isspace(c)) {
            if (!token.empty()) {
                tokens.push_back(token);
                token.clear();
            }
        } else {
            token += c;
        }
    }
    if (!token.empty()) {
        tokens.push_back(token);
    }
    return tokens;
}
