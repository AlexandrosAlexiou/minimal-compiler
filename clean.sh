# find generated files and delete them
RED='\033[91m'
GREEN='\033[92m'
NC='\033[0m' # No Color

# find generated files and delete them
echo "${RED}This will delete all mpcc generated files from ./tests folder. Are you sure?${NC} (${RED}Y${NC}/${GREEN}n${NC})"
read -r input
if [[  $input =~ ^[Y]$ ]]
then
# Do dangerous stuff
find ./tests -name "*.int" -type f -delete
find ./tests -name "*.c" -type f -delete
find . -name "*.out" -type f -delete
find ./tests -name "*.out" -type f -delete
find ./tests -name "*.asm" -type f -delete
fi