#!/bin/bash

ROOT_DIR=$(pwd)
EXTERNAL_DIR="${ROOT_DIR}/external"
ANTLR_JAR="antlr-4.13.2-complete.jar"
BUILD_DIR="${ROOT_DIR}/build"
GRAMMAR_DIR="${ROOT_DIR}/src/grammar"

mkdir -p "${BUILD_DIR}"
cp "${GRAMMAR_DIR}/lexererr.py" "${BUILD_DIR}/lexererr.py"

# Compile grammar files
echo "Compiling ANTLR grammar files..."
java -jar "${EXTERNAL_DIR}/${ANTLR_JAR}" \
    -Dlanguage=Python3 \
    -visitor \
    -no-listener \
    -o "${BUILD_DIR}" \
    "${GRAMMAR_DIR}"/*.g4

echo "ANTLR grammar files compiled to ${BUILD_DIR}"