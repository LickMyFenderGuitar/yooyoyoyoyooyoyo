#ifndef FLUX_RUNTIME_H
#define FLUX_RUNTIME_H

#include <string>

enum class RuntimeMode {
    INTERPRETER,
    PARSER
};

class FluxRuntime {
public:
    static RuntimeMode mode;
    static void use(std::string runtime);
};

#endif // FLUX_RUNTIME_H
