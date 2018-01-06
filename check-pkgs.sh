#!/bin/bash

PKGS="
python3-click
python3-requests
python3-scapy
"

ERROR=0

for pkg in $PKGS
do
    echo -n "checking $pkg... "
    status=$(dpkg -s $pkg > /dev/null 2>&1)
    if [ $? -ne 0 ]
    then
        echo "ERROR"
        ERROR=1
    else
        echo "OK"
    fi

done

if [ $ERROR -eq 0 ]
then
    echo "Good. You have all the needed packages"
fi


