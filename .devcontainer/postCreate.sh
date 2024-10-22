#!/bin/bash
CONFIG=${1:-host}
# move clang-format to home directory
[[ -f .clang-format ]] && mv .clang-format ~

# copy everyting except the src and include folders from the
# taget project to avoid overwriting any src/include files on rebuild
mkdir -p include src 
cp -rf $(ls -d ~/projects/cmake-$CONFIG/* | grep -Ev '/?(src|include)/?$') .

# remove .git repos that may cause warnings on first build with no src files
if ! test -f src/main.*; then
  echo "Remove .git folders on first build"
  rm -rf .git 2>/dev/null
  rm -rf *-[0-9][0-9][0-9]_exercises/.git 2>/dev/null
fi
