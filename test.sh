#!/bin/bash
INPUTFILE=$1
FILENAME=`basename $INPUTFILE`
NAME=chucu_${FILENAME}_

for i in `seq 1 10`;
do
    ./lk_generate_specimen.sh -i $INPUTFILE -o /home/chucu/Desktop/${NAME}${i}.exe -m -f
done 
