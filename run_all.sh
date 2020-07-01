#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

for i in {1..7}
do
  echo "${RED}Running test${i}.min${NC}"
  ./mppc.py tests/test$i.min
  printf '\n\n'
done