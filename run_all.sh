RED='\033[91m'
NC='\033[0m' # No Color

for i in {1..10}
do
  echo "${RED} Running test${i}.min ${NC}"
  ./mppc.py tests/test$i.min
  printf '\n\n'
done