// main.cpp
// See project README.md for disclaimer and additional information.
// Feabhas Ltd

#include <iostream>
#include "Timer.h"

int main()
{
    for(unsigned i=0; i< 5; ++i) {
        std::cout << "tick...\n";
        sleep(1000);
    };
}
