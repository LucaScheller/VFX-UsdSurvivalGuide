### Configuration ###
# Here we declare some custom variables that configure namings
set(USDSG_PROJECT_NAME UsdExamplesSchemas)

set(USDSG_EXAMPLESCHEMAS_USD_PLUGIN_NAME usdExampleSchemas)
set(USDSG_EXAMPLESCHEMAS_USD_CXX_CLASS_NAME UsdExampleSchemas)
set(USDSG_EXAMPLESCHEMAS_USD_PYTHON_MODULE_NAME UsdExampleSchemas)
set(USDSG_EXAMPLESCHEMAS_TARGET_LIB usdExampleSchemas)
set(USDSG_EXAMPLESCHEMAS_TARGET_PYTHON _${USDSG_EXAMPLESCHEMAS_TARGET_LIB})

# Arch
set(USDSG_ARCH_LIB_SUFFIX so)
# Houdini
set(USDSG_HOUDINI_ROOT $ENV{HFS})
set(USDSG_HOUDINI_LIB_DIR ${USDSG_HOUDINI_ROOT}/dsolib)
set(USDSG_HOUDINI_INCLUDE_DIR ${USDSG_HOUDINI_ROOT}/toolkit/include)
# Usd
set(USDSG_PXR_LIB_DIR ${USDSG_HOUDINI_ROOT}/dsolib)
set(USDSG_PXR_LIB_PREFIX "pxr_")
set(USDSG_PXR_INCLUDE_DIR ${USDSG_HOUDINI_INCLUDE_DIR})
# Python
set(USDSG_PYTHON_LIB_DIR ${USDSG_HOUDINI_ROOT}/python/lib)
set(USDSG_PYTHON_LIB python3.9)
set(USDSG_PYTHON_LIB_NUMBER python39)
set(USDSG_PYTHON_LIB_SITEPACKAGES ${USDSG_PYTHON_LIB_DIR}/${USDSG_PYTHON_LIB}/site-packages)
set(USDSG_PYTHON_INCLUDE_DIR ${USDSG_HOUDINI_INCLUDE_DIR}/${USDSG_PYTHON_LIB})
# Boost
set(USDSG_BOOST_NAMESPACE hboost)
set(USDSG_BOOST_INCLUDE_DIR "${USDSG_HOUDINI_INCLUDE_DIR}/${USDSG_BOOST_NAMESPACE}")
set(USDSG_BOOST_PYTHON_LIB ${USDSG_BOOST_NAMESPACE}_${USDSG_PYTHON_LIB_NUMBER})
# usdGenSchema plugInfo.json vars
set(PLUG_INFO_ROOT ".")
set(PLUG_INFO_LIBRARY_PATH "../lib/${USDSG_EXAMPLESCHEMAS_TARGET_LIB}.${USDSG_ARCH_LIB_SUFFIX}")
set(PLUG_INFO_RESOURCE_PATH ".")

### Init ###
cmake_minimum_required(VERSION 3.14 FATAL_ERROR)
project(${USDSG_PROJECT_NAME} VERSION 1.0.0 LANGUAGES CXX)

### CPP Settings ###
set(BUILD_SHARED_LIBS ON)
# Preprocessor Defines (Same as #define)
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=0 HBOOST_ALL_NO_LIB BOOST_ALL_NO_LIB)
# This is the same as set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHBOOST_ALL_NO_LIB -D_GLIBCXX_USE_CXX11_ABI=0")
# Compiler Options
add_compile_options(-fPIC -Wno-deprecated -Wno-deprecated-declarations -Wno-changes-meaning) # -Zc:inline-

### Packages ### (Settings for all targets)
# Houdini
link_directories(${USDSG_HOUDINI_LIB_DIR})
# Usd (Already provided via Houdini)
# link_directories(${USDSG_PXR_LIB_DIR})
# Python (Already provided via Houdini)
# link_directories(${USDSG_PYTHON_LIB_DIR})

### CPP Settings ###
SET(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/dist" CACHE PATH "Default install dir " FORCE)

### Targets ###
## Target library > usdSchemaExamples ##
add_library(${USDSG_EXAMPLESCHEMAS_TARGET_LIB}
    SHARED
        src/complex.cpp
        src/paramsAPI.cpp
        src/simple.cpp
        src/tokens.cpp
)
# Libs
target_link_libraries(${USDSG_EXAMPLESCHEMAS_TARGET_LIB}
    ${USDSG_PXR_LIB_PREFIX}tf
    ${USDSG_PXR_LIB_PREFIX}vt
    ${USDSG_PXR_LIB_PREFIX}usd
    ${USDSG_PXR_LIB_PREFIX}sdf
)
# Headers
target_include_directories(${USDSG_EXAMPLESCHEMAS_TARGET_LIB}
    PUBLIC
    ${USDSG_BOOST_INCLUDE_DIR}
    ${USDSG_PYTHON_INCLUDE_DIR}
    ${USDSG_PXR_INCLUDE_DIR}
)
# Props
# Remove default "lib" prefix
set_target_properties(${USDSG_EXAMPLESCHEMAS_TARGET_LIB} PROPERTIES PREFIX "")
# Preprocessor Defines (Same as #define)
target_compile_definitions(${USDSG_EXAMPLESCHEMAS_TARGET_LIB}
    PRIVATE
        # USD Plugin Internal Namings
        MFB_PACKAGE_NAME=${USDSG_EXAMPLESCHEMAS_USD_PLUGIN_NAME}
)
# Install
configure_file(src/plugInfo.json plugInfo.json)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/plugInfo.json DESTINATION resources)
install(FILES src/generatedSchema.usda DESTINATION resources)
install(TARGETS ${USDSG_EXAMPLESCHEMAS_TARGET_LIB} RUNTIME DESTINATION lib)

## Target library > usdSchemaExamples Python ##
add_library(${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON}
    SHARED
        src/wrapComplex.cpp
        src/wrapParamsAPI.cpp
        src/wrapSimple.cpp
        src/wrapTokens.cpp
        src/module.cpp
        src/moduleDeps.cpp
)
# Libs
target_link_libraries(${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON}
    ${USDSG_EXAMPLESCHEMAS_TARGET_LIB}
    ${USDSG_BOOST_PYTHON_LIB}
)
# Headers
target_include_directories(${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON}
    PUBLIC
        ${USDSG_BOOST_INCLUDE_DIR}
        ${USDSG_PYTHON_INCLUDE_DIR}
        ${USDSG_PXR_INCLUDE_DIR}
)
# Props
# Remove default "lib" prefix
set_target_properties(${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON} PROPERTIES PREFIX "")
# Preprocessor Defines (Same as #define)
target_compile_definitions(${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON}
    PRIVATE
        # USD Plugin Internal Namings
        MFB_PACKAGE_NAME=${USDSG_EXAMPLESCHEMAS_USD_PLUGIN_NAME}
        MFB_PACKAGE_MODULE=${USDSG_EXAMPLESCHEMAS_USD_PYTHON_MODULE_NAME}
)
# Install
install(FILES src/__init__.py DESTINATION lib/python/${USDSG_EXAMPLESCHEMAS_USD_PYTHON_MODULE_NAME})
install(
    TARGETS ${USDSG_EXAMPLESCHEMAS_TARGET_PYTHON}
    DESTINATION lib/python/${USDSG_EXAMPLESCHEMAS_USD_PYTHON_MODULE_NAME}
)

# Status
message(STATUS "--- Usd Example Schemas Instructions Start ---")
message(NOTICE "To use the compiled files, set the following environment variables:")
message(NOTICE "export PYTHONPATH=${CMAKE_INSTALL_PREFIX}/lib/python:${USDSG_PYTHON_LIB_SITEPACKAGES}:$PYTHONPATH")
message(NOTICE "export PXR_PLUGINPATH_NAME=${CMAKE_INSTALL_PREFIX}/resources:$PXR_PLUGINPATH_NAME")
message(NOTICE "export LD_LIBRARY_PATH=${CMAKE_INSTALL_PREFIX}/lib:${HFS}/python/lib:${HFS}/dsolib:$LD_LIBRARY_PATH")
message(STATUS "--- Usd Example Schemas Instructions End ---\n")

