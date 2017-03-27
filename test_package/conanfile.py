from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "kmaragon")


class Bzip2TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "bzip2/1.0.6@%s/%s" % (username, channel)
    generators = "cmake"

    def configure(self):
        self.options['bzip2'].shared = True

    def build(self):
        cmake = CMake(self.settings)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
        cmake.build(self)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
