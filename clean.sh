#!/usr/bin/env bash

# find generated files and delete them

find ./tests -name "*.int" -type f -delete
find ./tests -name "*.c" -type f -delete
find . -name "*.out" -type f -delete
find ./tests -name "*.asm" -type f -delete
