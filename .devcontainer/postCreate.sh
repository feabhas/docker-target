#!/bin/bash
CONFIG=${1:-host}
# move clang-format to home directory
[[ -f .clang-format ]] && mv .clang-format ~

# copy everyting except the src and include folders from the
# taget project to avoid overwriting any src/include files on rebuild
mkdir -p include src 
cp -r $(ls -d ~/projects/cmake-$CONFIG/* | grep -Ev '/?(src|include)/?$') .

# reset git repro simulating a shallow fork of the project
if [[ ! -d .git ]]; then 
  git init -b main
fi
git config --global --add safe.directory /home/feabhas/workspace
git config core.safecrlf false
git add -A
