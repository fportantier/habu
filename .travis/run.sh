#!/bin/sh

pip install -e .

for cmd in $(whereis habu | tr " " "\n" | grep "habu\.")
do
    echo $cmd
    $cmd --help > /dev/null
    if [ "$?" != "0" ]
    then
        echo "Error running help for $cmd"
        exit 1
    fi
done

