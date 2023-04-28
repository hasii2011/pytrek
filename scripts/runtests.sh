#!/bin/bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

# python3 -Wdefault -m tests.TestAll
python3 -m tests.TestAll
