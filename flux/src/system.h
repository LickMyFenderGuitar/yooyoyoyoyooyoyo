#ifndef FLUX_SYSTEM_H
#define FLUX_SYSTEM_H

#include <string>

class System {
public:
    static std::string in();
    static void println(const std::string& msg);
};

#endif // FLUX_SYSTEM_H
