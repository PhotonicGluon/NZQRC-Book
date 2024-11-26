#!/bin/sh

# Check if a commit is being processed
if [ -e .commit ]
    then

    # Mark that the commit is done
    rm .commit

    # Update the commit hash
    python code/commit/update_commit_hash.py
fi
exit
