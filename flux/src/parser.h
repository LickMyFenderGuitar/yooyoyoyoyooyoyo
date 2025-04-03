#ifndef FLUX_PARSER_H
#define FLUX_PARSER_H

#include <vector>
#include <string>

class Parser {
public:
    static void parse(const std::vector<std::string>& tokens);
};

#endif // FLUX_PARSER_H
