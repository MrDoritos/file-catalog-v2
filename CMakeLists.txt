
cmake_minimum_required(VERSION 3.10)
project(file-catalog)

set(CMAKE_CXX_STANDARD 17)

set(CPP_HTTPLIB_LIBRARY_PATH "../cpp-httplib/")

add_executable(file-catalog
    main.cpp
    server.cpp
    catalog.cpp
)

find_package(nlohmann_json REQUIRED)
target_link_libraries(file-catalog PRIVATE nlohmann_json::nlohmann_json)

#find_package(cpp-httplib REQUIRED)
find_library(CPP_HTTPLIB_LIBRARY
	NAMES httplib
	PATHS ${CPP_HTTPLIB_LIBRARY_PATH}
	REQUIRED)
target_link_libraries(file-catalog PRIVATE ${CPP_HTTPLIB_LIBRARY})
