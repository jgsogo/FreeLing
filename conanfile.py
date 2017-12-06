#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class FreeLingConan(ConanFile):
    name = "FreeLing"
    version = "0.0.0"
    url = "https://github.com/TALP-UPC/FreeLing"
    description = "FreeLing, an open source language analysis tool suite"
    license = "https://github.com/TALP-UPC/FreeLing/blob/master/COPYING"
    exports_sources = ["CMakeLists.txt", "COPYING", "src/*",]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], }
    default_options = "shared=True"
    generators = "cmake"
    
    requires = "zlib/1.2.11@conan/stable", "Boost/1.64.0@conan/stable", "icu/59.1@bincrafters/stable"

    def source(self):
        # This should be in CMakeLists.txt, but do not want to be intrusive right now
        tools.replace_in_file("./CMakeLists.txt", "project(FreeLing)", 
        '''project(FreeLing)
           include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
           conan_basic_setup()
        ''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=".")
        cmake.build()

    def package(self):
        with tools.chdir("."):
            self.copy(pattern="COPYING")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
