#!/usr/bin/env bash
#
#  Assumes python 3 is on PATH
#
clear

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

if [[ $# -eq 0 ]] ; then
        echo "in alias mode"
        rm -rf build dist
        python3 setup.py py2app --alias --no-strip  --iconfile pytrek/resources/images/StarTrek.icns
else
    if [[ ${1} = 'deploy' ]] ; then
            echo "in deploy mode"
            rm -rf build dist
            python3 setup.py py2app --packages=arcade --iconfile pytrek/resources/images/StarTrek.icns
    else
        echo "Unknown command line arguments"
    fi
rm -rf src/UNKNOWN.egg-info
fi
