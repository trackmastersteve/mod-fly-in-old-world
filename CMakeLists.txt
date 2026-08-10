# CMakeLists.txt

# Find all C++ files in the src directory
file(GLOB_RECURSE sources_mod_fly src/*.cpp src/*.h)

# Register the module with modern AzerothCore
target_sources(modules PRIVATE ${sources_mod_fly})
