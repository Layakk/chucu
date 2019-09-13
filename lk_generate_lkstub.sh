#!/bin/bash
#######
# INLCUDE SECTION
#######

. lk_option_parser.sh || exit 1


EXECFOLDER=/home/chucu/Desktop/chucu_test/chucu/
UPXFOLDER=upx-3.91-src/
UPXLISTEXE=./upx_listlabels.out
STUBFULL=i386-win32.pe.S.FULLINONE
LKSTUB=i386-win32.pe.S.LKSTUB
STUBSRCFOLDER=upx-3.91-src/src/stub/src/
TMPEXE=/tmp/novale_packed.exe
TMPFILE=stub_sec_list.txt
#######
# PARAMETERS SECTION
#######
#INPUT FILE
add_program_option "-i" "--input" "Input file path to be packed." "YES" "YES"

####
parse_program_options $@

show_program_usage "-h"

is_option_present "-h" && exit 0

###
echo "Processing parameters..."
#INPUT FILE
FULLINPUTPATH=`get_option_value "-i"`

#Check if output file exists and remove it
echo "Checking if input file exists..."
if [[ ! -f "$FULLINPUTPATH" ]]
then
        printf "[ERROR] Input file does not exists. Exiting...\n\n"
        exit 1
fi
echo "Done."

$UPXLISTEXE -1 -v -k -o$TMPEXE $FULLINPUTPATH | grep "LIST" > $EXECFOLDER$TMPFILE
rm $TMPEXE

./lk_build_lkstub.py $EXECFOLDER$STUBFULL $EXECFOLDER$LKSTUB $EXECFOLDER$TMPFILE
rm $EXECFOLDER$TMPFILE


