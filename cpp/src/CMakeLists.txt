# CMake のバージョンを設定
cmake_minimum_required(VERSION 2.8)

# プロジェクト名
project(test_project)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)
FetchContent_Declare(matplotplusplus
  GIT_REPOSITORY https://github.com/alandefreitas/matplotplusplus
  GIT_TAG origin/master) # or whatever tag you want
FetchContent_GetProperties(matplotplusplus)

if(NOT matplotplusplus_POPULATED)
  FetchContent_Populate(matplotplusplus)
  add_subdirectory(${matplotplusplus_SOURCE_DIR} ${matplotplusplus_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()

include_directories(/usr/local/include)
add_executable(a.out simulate.cpp)
target_link_libraries(a.out PUBLIC matplot)