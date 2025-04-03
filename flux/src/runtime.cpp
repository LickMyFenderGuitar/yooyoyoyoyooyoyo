#include "runtime.h"
#include <iostream>

RuntimeMode FluxRuntime::mode = RuntimeMode::INTERPRETER;

void FluxRuntime::use(std::string runtime) {
    if (runtime == "interp") {
        mode = RuntimeMode::INTERPRETER;
        std::cout << "[Flux] Running in Interpreter mode." << std::endl;
    } else if (runtime == "parser") {
        mode = RuntimeMode::PARSER;
        std::cout << "[Flux] Running in Parser mode." << std::endl;
    } else {
        std::cerr << "[Flux] Unknown runtime mode: " << runtime << std::endl;
    }
}
