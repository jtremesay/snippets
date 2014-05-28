#!/bin/bash

old_is_connected=0;
while true
do

    fping -q 8.8.8.8
    [[ $? -eq 0 ]] && $new_is_connected=1 || $new_is_connected=0
    if [ $old_is_connected -neq $new_is_connected ]
    then
        $old_is_connected=$new_is_connected
        if [ $old_is_connected -eq 1 ]
        then
            echo "connexion up"
        else
            echo "connexion down"
        fi
    fi

    sleep 1
done