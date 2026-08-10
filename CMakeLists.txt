# CMakeLists.txt
set(TC_MODULE_NAME "mod-fly-in-old-world")

# Find all C++ files in the src directory
file(GLOB_RECURSE sources src/*.cpp src/*.h)

# Register the module with AzerothCore
ac_add_script_module("${TC_MODULE_NAME}" "${sources}")
