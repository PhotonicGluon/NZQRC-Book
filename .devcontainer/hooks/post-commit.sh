#!/bin/sh

# Check if a commit is being processed
if [ -e .commit ]
    then
    rm .commit
    # git add committest.txt
    # git commit --amend -C HEAD --no-verify
fi
exit
