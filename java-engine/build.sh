#!/usr/bin/env bash
set -euo pipefail
mkdir -p out
find src/main/java -name "*.java" > sources.txt
javac -d out @sources.txt
rm sources.txt
echo "Build completed. Classes are in out/."
