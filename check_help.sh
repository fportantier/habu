#!/bin/sh

for cmdfile in $(ls habu/cli/cmd_*.py)
do
    python3 $cmdfile --help > /dev/null 2>&1
    if [ "$?" != "0" ]
    then
        echo "Error running help for $cmdfile"
    fi
done

