#!/bin/bash

loglevel_label=("[DEBUG  ]" "[INFO   ]" "[WARNING]" "[ERROR  ]")
loglevel_style=("\033[2;37m" "\033[0;38m" "\033[0;33m" "\033[0;31m")

# Define your function here
LK_LOG () {
   printf "${loglevel_style[$1]}[LK] ${loglevel_label[$1]} $2\n"
}

LK_EXIT() {
    printf "\033[0;38m"
    exit $1
}

LK_SPINNER() {
    ($@) > /dev/null &
    PID=$!
    i=1
    sp="/-\|"
    echo -n ' '
    while [ -d /proc/$PID ]
    do
        sleep 0.1
        printf "\b${sp:i++%${#sp}:1}"
    done
    printf "\b"
}
