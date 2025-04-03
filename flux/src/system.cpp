#include "system.h"
#include <iostream>

std::string System::in() {
    std::string input;
    std::cout << "[Flux] Enter input: ";
    std::getline(std::cin, input);
    return input;
}

void System::println(const std::string& msg) {
    std::cout << msg << std::endl;
}
