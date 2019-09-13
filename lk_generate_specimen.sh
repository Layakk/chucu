#!/bin/bash
#######
# INLCUDE SECTION
#######
#export PATH=$PATH":/home/chucu/Documents/bin-upx-20130920/"
scriptpath=`realpath $0`
SCRIPTDIR=`dirname $scriptpath`

cd $SCRIPTDIR

. lk_option_parser.sh || exit 1
. lk_logger.sh || exit 1

UPXFOLDER=$SCRIPTDIR/upx-3.91-src
UPXSRCFOLDER=$SCRIPTDIR/upx-3.91-src/src
STUBFOLDER=$SCRIPTDIR/upx-3.91-src/src/stub/src
STUBNAME=$STUBFOLDER/i386-win32.pe.S

UPXEXE=./upx.out
UPXLISTEXE=./upx_listlabels.out

STUBFULL=$SCRIPTDIR/i386-win32.pe.S.FULLINONE
TMPDIR=$SCRIPTDIR/tmp
LKSTUB=$TMPDIR/i386-win32.pe.S.LKSTUB
LKTMPSTUB=$TMPDIR/i386-win32.pe.S.LKTMPSTUB
TMPLISTFILE=$TMPDIR/stub_list.txt
TMPEXE=$TMPDIR/packed.exe

#######
# PARAMETERS SECTION
#######
#INPUT FILE
add_program_option "-i" "--input" "Fichero de entrada a empaquetar." "YES" "YES"
#OUTPUT FILE
add_program_option "-o" "--output" "Fichero de salida empaquetado. Si no se especifica sera el de entrada con prefijo 'p_'." "NO" "YES"
#BASURA
add_program_option "-t" "--trash" "Activa el agregado de texto plano para reducir entropia. Se debe indicar el numero de Bytes." "NO" "YES"
add_program_option "-b" "--trashfile" "Indica el fichero del que extraer texto plano." "NO" "YES"
#CIFRADO CODIGO
add_program_option "-c" "--code" "Activa la opcion de cifrado de codigo." "NO" "NO"
#Resources Ciphering
add_program_option "-r" "--resources" "Activa la opcion de cifrado de recursos." "NO" "NO"
#Resources Ciphering
add_program_option "-s" "--resourcessize" "Cota inferior del cifrado de recursos. Default 0." "NO" "YES"
#Resources Ciphering
add_program_option "-p" "--resourcestop" "Cota superior del cifrado de recursos. Default 0." "NO" "YES"
#Force removing output file
add_program_option "-f" "--force" "Fuerza el borrado del fichero de salida (si existe) sin preguntar." "NO" "NO"
#Show help
add_program_option "-h" "--help" "Mustra ayuda help." "NO" "NO"
#Mix Stub Code
add_program_option "-m" "--mix" "Activa el chucu-chucu. Parametro en, por ejemplo, formato [3,5]: minimo 3 instrucciones por bloque y maximo 5." "NO" "YES"
#Debug mode, don't remove tmp files.
add_program_option "-d" "--debug" "Modo Debug (No borra los ficheros temporales)." "NO" "NO"

####
parse_program_options $@

show_program_usage "-h"

is_option_present "-h" && exit 0

###
#echo "Processing parameters..."
LK_LOG 1 "Processing parameters..."
#INPUT FILE
FULLINPUTPATH=`get_option_value "-i"`

#OUTPUT FILE
if is_option_present "-o"
then
    OUTPUTFILE=`get_option_value "-o"`

else
    EXECUTABLEPATH=`dirname $FULLINPUTPATH`
    EXECUTABLENAME=`basename $FULLINPUTPATH`
    OUTPUTFILE=$EXECUTABLEPATH"/p_"$EXECUTABLENAME
fi

#MULTIPLIER
if is_option_present "-t"
then
    TRASH_LENGTH=`get_option_value "-t"`
    TRASHFLAGS="-DTRASH_LENGTH=$TRASH_LENGTH"
    if is_option_present "-b"
    then
        TRASH_FILE=`get_option_value "-b"`
        TRASHFLAGS+=" -DTRASH_FILE=$TRASH_FILE"
    fi 
else
    TRASHFLAGS=
fi

if is_option_present "-c"
then
    CIFRADOON="YES"
    CIFRADOFLAGS="-DCIFRADOON"
    CIFRADOPARAM="--lkcipher"
else
    CIFRADOON="NO"
    CIFRADOFLAGS=
    CIFRADOPARAM=
fi

#Resources Ciphering
if is_option_present "-r"
then
    RESCIFON="YES"
    RESCIFFLAGS="-DRESCIFON"
    RESCIFDATAFLAGS="-DRESCIFON"
    RESCIFPARAM="--lkresources"
    if is_option_present "-s"
    then
        OFFSET_BOT=`get_option_value "-s"`
        RESCIFDATAFLAGS+=" -DRESNOTCIPHERED=$OFFSET_BOT"
    else
        OFFSET_BOT=0
        RESCIFDATAFLAGS+=" -DRESNOTCIPHERED=$OFFSET_BOT"
    fi
    if is_option_present "-p"
    then
        OFFSET_TOP=`get_option_value "-p"`
        RESCIFDATAFLAGS+=" -DRESNOTCIPHEREDTOP=$OFFSET_TOP"
    else
        OFFSET_TOP=0
        RESCIFDATAFLAGS+=" -DRESNOTCIPHEREDTOP=$OFFSET_TOP"
    fi
else
    RESCIFON="NO"
    RESCIFFLAGS=
    RESCIFDATAFLAGS=
fi

MIXSTUB=false
MIXLIMIT=
if is_option_present "-m"
then
    MIXSTUB=true 
    MIXLIMIT=`get_option_value "-m"`
fi

DEBUGMODE=false 
if is_option_present "-d"
then
    DEBUGMODE=true 
fi
#echo "Parameters processed successfully!"
#echo ""
#echo "Chosen Parameters:"
#printf "  Input file path:           %s\n" "$FULLINPUTPATH"
#printf "  Output file Path:          %s\n" "$OUTPUTFILE"
#printf "  Trash size in bytes:       %s\n" "$TRASH_LENGTH"
#printf "  Trash file:                %s\n" "$TRASH_FILE"
#printf "  Code ciphering:            %s\n" "$CIFRADOON"
#printf "  Resources ciphering:       %s\n" "$RESCIFON"
#printf "  Resources bot offset:      %s\n" "$OFFSET_BOT"
#printf "  Resources top offset:      %s\n" "$OFFSET_TOP"

#echo ""


LK_LOG 1 "Parameters processed successfully!"
LK_LOG 1 "Chosen Parameters:"
LK_LOG 1 "  Input file path:           $FULLINPUTPATH"
LK_LOG 1 "  Output file Path:          $OUTPUTFILE"
LK_LOG 1 "  Trash size in bytes:       $TRASH_LENGTH"
LK_LOG 1 "  Trash file:                $TRASH_FILE"
LK_LOG 1 "  Code ciphering:            $CIFRADOON"
LK_LOG 1 "  Resources ciphering:       $RESCIFON"
LK_LOG 1 "  Resources bot offset:      $OFFSET_BOT"
LK_LOG 1 "  Resources top offset:      $OFFSET_TOP"
LK_LOG 1 "  Mix mode:                  $MIXSTUB"
LK_LOG 1 "  Mix limit:                 $MIXLIMIT"
LK_LOG 1 "  Debug mode:                $DEBUGMODE"

LK_LOG 1 ""
#Check if output file exists and remove it
#echo "Checking if input file exists..."
LK_LOG 1 "Checking if input file exists..."
if [[ ! -f "$FULLINPUTPATH" ]]
then
	#printf "[ERROR] Input file does not exists. Exiting...\n\n"
	#exit 1
	LK_LOG 3 "Input file does not exists. Exiting..."
	LK_EXIT 1
fi
#echo "Done."
LK_LOG 1 "Done."

#Check if output file exists and remove it
#echo "Checking if output file exists..."
LK_LOG 1 "Checking if output file exists..."
if [[ -f $OUTPUTFILE ]]
then
    #echo "Output file $OUTPUTFILE exists."
    LK_LOG 1 "Output file $OUTPUTFILE exists."
    if ! is_option_present "-f"
    then 
        read
    fi
    #echo "Removing it..."
    LK_LOG 1 "Removing it..."
    rm $OUTPUTFILE
    #TODO Revisar este control de errores. NO FUNCIONA!
    if [[ $? -ne 0 ]]
    then
	#printf "[ERROR] Can't remove output file. Exiting...\n\n"
	#exit 1
	LK_LOG 3 "Can't remove output file. Exiting..."
	LK_EXIT 1
    fi
fi
#echo "Done."
LK_LOG 1 "Done."
#echo ""

#######
# BUILDING SECTION
#######
CURRENTFOLDER=`pwd`
#echo "Starting building section..."
LK_LOG 1 "Starting building section..."

#echo "Starting generate custom stub..."
LK_LOG 1 "Starting generate custom stub..."
cd $SCRIPTDIR

mkdir -p $TMPDIR

#echo "$UPXLISTEXE $CIFRADOPARAM $RESCIFPARAM -1 -v -k -o$TMPEXE $FULLINPUTPATH | grep "LIST" > $TMPLISTFILE"
$UPXLISTEXE $CIFRADOPARAM $RESCIFPARAM -1 -v -k -o$TMPEXE $FULLINPUTPATH | grep "LIST" > $TMPLISTFILE
rm $TMPEXE

./lk_build_lkstub.py $STUBFULL $LKTMPSTUB $TMPLISTFILE

if [ "$DEBUGMODE" == false ]
then
    echo "HELLO"
    rm $TMPLISTFILE
fi

#echo "Done!"
LK_LOG 1 "Done!"

if [[ "$MIXSTUB" == true ]]
then
LK_LOG 1 "Chucu chucu chucu..."
./chucu_chucu.py -i $LKTMPSTUB -o $LKSTUB -l $MIXLIMIT
LK_LOG 1 "Done!"
else
    LKSTUB=$LKTMPSTUB
fi

#Copying stub output to correctly stub src
cp $LKSTUB $STUBNAME

if [ "$DEBUGMODE" == false ]
then
    if [ -f $LKTMPSTUB ]
    then
        rm $LKTMPSTUB
    fi
    if [ -f $LKTMPSTUB ]
    then
        rm $LKSTUB
    fi
fi

#echo "Building stub section..."
LK_LOG 1 "Building stub section..."
cd $STUBFOLDER 
#make clean > /dev/null
#make CUSTOMVARS="$CIFRADOFLAGS $RESCIFFLAGS"
#make
#make > /dev/null &

if [ "$DEBUGMODE" == false ]
then
    LK_SPINNER make
else
    make
fi

if [[ $? -ne 0 ]]
then
    #printf "[ERROR] Can't build stub section. Exiting...\n\n"
    #exit 1
    LK_LOG 3 "Can't build stub section. Exiting..."
    LK_EXIT 1
fi
#echo "Done."
LK_LOG 1 "Done."

#echo "Building UPX Custom code..."
LK_LOG 1 "Building UPX Custom code..."
cd $UPXSRCFOLDER
touch p_w32pe.cpp

#make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS"
#make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS" > /dev/null

if [ "$DEBUGMODE" == false ]
then
    #echo make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS"
    #LK_SPINNER make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS"
    make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS"
else
    make CUSTOMVARS="$TRASHFLAGS $CIFRADOFLAGS $RESCIFDATAFLAGS"
fi

if [[ $? -ne 0 ]]
then
    #printf "[ERROR] Can't build UPX code. Exiting...\n\n"
    #exit 1
    LK_LOG 3 "Can't build UPX code. Exiting..."
    LK_EXIT 1
fi
#echo "Done."
LK_LOG 1 "Done."

#echo "Building section ends successfully."
LK_LOG 1 "Building section ends successfully."

#######
# RUNNING SECTION
#######
#echo "Running packing process..."
LK_LOG 1 "Running packing process..."
cd $UPXSRCFOLDER
$UPXEXE -1 -v -k -o$OUTPUTFILE $FULLINPUTPATH
if [[ $? -ne 0 ]]
then
    #printf "[ERROR] Can't execute UPX properly. Exiting...\n\n"
    #exit 1
    LK_LOG 3 "Can't execute UPX properly. Exiting..."
    LK_EXIT 1
fi
#echo "Done."
LK_LOG 1 "Done."
