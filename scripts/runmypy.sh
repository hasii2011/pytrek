#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

# cd src > /dev/null 2>&1
echo "current: `pwd`"

# mypy --config-file .mypi.ini --show-error-codes --no-color-output pytrek tests
# mypy --config-file .mypi.ini --show-error-codes --html-report mypy-report pytrek tests
mypy --config-file .mypi.ini --show-error-codes --check-untyped-defs pytrek tests
status=$?

echo "Exit with status: ${status}"
exit ${status}

