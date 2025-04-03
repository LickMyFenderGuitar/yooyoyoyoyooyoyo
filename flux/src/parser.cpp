#include "parser.h"
#include <iostream>

void Parser::parse(const std::vector<std::string>& tokens) {
    std::cout << "[Flux] Parsing code..." << std::endl;
    for (const auto& token : tokens) {
        std::cout << "[Token] " << token << std::endl;
    }
}
