#!/bin/bash

# Run pytest and store its exit status
# If specific filename then run only that test if not then run on all files
if [ -z "$1" ]; then
  pylint -E **/*.py
else
  pylint -E "$1"
fi
result=$?

if [ $result -ne 0 ] && [ $result -ne 5 ]; then
    exit 1 # Exit with an error status
else
    exit 0 # Exit with a success status
fi

if [ -z "$1" ]; then
  pytest -q -x -rN -k $(basename $1)
else
  pytest -q -x -rN
fi
result=$?

# pytest exit codes:
# 0: All tests were collected and passed successfully
# 1: Tests were collected and run but some of the tests failed
# 2-4: Test execution was interrupted by the user or internal error
# 5: No tests were collected

# Check the exit status not 0 or 5
if [ $result -ne 0 ] && [ $result -ne 5 ]; then
    exit 1 # Exit with an error status
else
    exit 0 # Exit with a success status
fi

