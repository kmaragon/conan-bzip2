#include <iostream>
#include <bzlib.h>

int main() {
    std::cout << BZ2_bzlibVersion() << std::endl;
}
