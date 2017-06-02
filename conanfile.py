from conans import ConanFile, tools
import os, re, glob, shutil


class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    license = "BSD Style"
    url = "https://github.com/kmaragon/conan-bzip2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    description = "A Conan package for bzip2 that can be used with an executable without having it clobbered"

    ZIP_FOLDER_NAME = "bzip2-%s" % version

    def source(self):

        zip_name = "bzip2-%s.tar.gz" % self.version
        tools.download("http://www.bzip.org/%s/%s" % (self.version, zip_name), zip_name)
        tools.check_md5(zip_name, "00b516f4704d4a7cb50a1d97e6e8e15b")
        tools.unzip(zip_name)

        os.unlink(zip_name)

        makefile = self.ZIP_FOLDER_NAME + "/Makefile"
        makeshared = self.ZIP_FOLDER_NAME + "/Makefile-libbz2_so"
        tools.replace_in_file(makefile, "PREFIX=", "PREFIX?=")
        tools.replace_in_file(makeshared, "PREFIX=", "PREFIX?=")

    def build(self):
        current_dir = os.getcwd()
        finished_package = current_dir + "/pkg"

        make_options = os.getenv("MAKEOPTS") or ""
        if not re.match("/[^A-z-a-z_-]-j", make_options):
            cpucount = tools.cpu_count()
            make_options += " -j %s" % (cpucount * 2)

        make_options += ' PREFIX="%s" ' % finished_package
        if self.options.shared:
            self.run("mkdir -p pkg/lib && cd %s && make clean && make -f Makefile-libbz2_so %s" % (self.ZIP_FOLDER_NAME, make_options))
            for file in glob.glob('%s/*bz2.so.*' % self.ZIP_FOLDER_NAME):
                shutil.move(file, "pkg/lib")
        else:
            self.run("cd %s && make %s install" % (self.ZIP_FOLDER_NAME, make_options))

    def package(self):
        self.copy("*", dst="lib", src="pkg/lib", links=True)
        self.copy("*", dst="bin", src="pkg/bin", links=True)
        self.copy("*", dst="include", src="pkg/include", links=True)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["bz2"]
        else:
            self.cpp_info.libs = ["libbz2.a"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
