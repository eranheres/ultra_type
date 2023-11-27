#!/bin/bash

# Run pytest and store its exit status
# shellcheck disable=SC2046
poetry run pytest -q -x -rN -k $(basename $1)
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

