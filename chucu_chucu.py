#!/usr/bin/python
import re
import random
import getopt
import sys
####
# GLOBAL
####
global block_count
block_count = 0


####
# LOG
####
#global loglevel
loglevel=1  # 0 DEBUG, 1 INFO, 2 WARNING, 3 ERROR
#global loglevel_label
loglevel_label=["[DEBUG  ]",
                "[INFO   ]",
                "[WARNING]",
                "[ERROR  ]"]

loglevel_style=["\033[2;37m",
                "\033[0;38m",
                "\033[0;33m",
                "\033[0;31m"]
                
def LK_EXIT(exit_code):
    print "\033[0;38m"
    exit(exit_code)

def LK_LOG(level, msg):
    if(level >= loglevel):
        print loglevel_style[level] + "[LK] " + loglevel_label[level] + " " + msg

####
# FUNCTIONS
####

## DEBUG FUNCTIONS
def printSectionToFile(section, filename, flags):
    #print "[LK] [DEBUG] Writing section file " + filename
    LK_LOG(0, "Escribiendo fichero de seccion " + filename)
    fout = open(filename,flags)
    # Check if open
    if fout.closed:
        #print "[LK] [DEBUG] Can't open output file: " + filename
        LK_LOG(0, "No se puede abrir el fichero de salida: " + filename + ". Saliendo...")
        LK_EXIT(1)

    for line in section:
        fout.write(line) 


    #print "[LK] [DEBUG] Writing file ends"
    LK_LOG(0, "Escritura de fichero acabada.")

    fout.close()


def printBlocksToFile(section_list, blocks, filename):
    #print "[LK] [DEBUG] Writing blocks to file."
    LK_LOG(0, "Escribiendo bloqes a un fichero.")
    fout = open(filename,'a+')
    # Check if open
    if fout.closed:
        #print "[LK] [DEBUG] Can't open output file: " + filename
        LK_LOG(0, "No se puede abrir el fichero de salida: " + filename + ". Saliendo...")
        LK_EXIT(1)

    for section_name in section_list:
        #print "[LK] [DEBUG] Printing section " + section_name
        LK_LOG(0, "Escribiendo seccion " + section_name)
        fout.write("section         " + section_name + "\n")
        for section in blocks[section_name]:
            for line in section:
                fout.write(line) 


    #print "[LK] [DEBUG] Writing file ends"
    LK_LOG(0, "Escritura del fichero acabada.")
    fout.close()



## REAL FUNCTIONS
#Check if line contains a pattern.
def checkLine(line, LK_PATTERN):
    match = re.match(LK_PATTERN, line)
    if(match == None):
        return False

    return True

#Parsea seciones dividiendolas en bloques por etiquetas y anadiendo saltos entre bloques.
def parseSection(section):
    #print "[LK] [INFO] Parsing section and inserting jumps between code blocks..."
    LK_LOG(0, "Parseando seccion e insertando 'jmp' entre bloques de codigo...")
    lk_blck         = list()
    lk_curr_blck    = list()

    for line in section:
        #print "[DEBUG] " + line[:-1]
        LK_LOG(0, line[:-1])
        if(checkLine(line, LK_ASM_SECTION)):
            #print "[DEBUG] New block found."
            LK_LOG(0, "Nuevo bloque encontrado!")
            if(len(lk_curr_blck)!=0):
                if(checkLine(lk_curr_blck[-1], LK_ASM_JMP)):
                    #print "[DEBUG] Blocks end with inconditional jump."
                    LK_LOG(0, "El bloque ya acaba con un salto incondicional. Continua sin anadir salto.")
                    None
                else:
                    #print "[DEBUG] Ending block inserting jump."
                    LK_LOG(0, "Insertando salto al final del bloque.")
                    lk_curr_blck.append("                jmp     " + line.split(":",1)[0] + "\n")
                lk_blck.append(lk_curr_blck)
                #print "[DEBUG] Initializing block " + line.split(":",1)[0]
                LK_LOG(0, "Inicializando nuevo bloque: " + line.split(":",1)[0])
                lk_curr_blck    = list()
            else:
                #print "[DEBUG] Block is empty. Do nothing."
                LK_LOG(0, "El bloque esta vacio. No se hace nada")
            lk_curr_blck.append(line)
        elif(checkLine(line, LK_ASM_INSTR)):
            lk_curr_blck.append(line)
        elif(checkLine(line, LK_BLANK_LINE)):
            None
        else:
            #print "[ERROR] Breaking loop because checkline does not match"
            LK_LOG(3, "Estructura de linea no conocida. Saliendo del bucle.")
            break

        line = lk_input_stub.readline()

    lk_blck.append(lk_curr_blck)
    #print "[LK] [INFO] Done!"
    LK_LOG(0, "HECHO!")
    return lk_blck

def splitCodeblocks(blocks_section):
    global block_count
    random.seed()
    lk_blck_tmp=blocks_section
    lk_blck=list()

    #print "[LK] [INFO] RANDOM: " + str(LK_MIN_INSTR) + "  " + str(LK_MAX_INSTR)
    LK_LOG(0, "Valores aleatorios entre " + str(LK_MIN_INSTR) + " y " + str(LK_MAX_INSTR))

    curr_instr_count = random.randint(LK_MIN_INSTR, LK_MAX_INSTR)
    for block in lk_blck_tmp:
        split_block_ends=False
        while not split_block_ends:
            if(len(block) > curr_instr_count):
                #print "[LK] [DEBUG] Splitting block " + block[0].split(":",1)[0]
                LK_LOG(0, "Dividiendo bloque: " + block[0].split(":",1)[0])
                count=0
                lk_sub_blk1=list()
                lk_sub_blk2=list()
                for instr in block:
                    #print "[LK] [DEBUG] count: " + str(count)
                    LK_LOG(0, "Contador: " + str(count)) 
                    if(count < curr_instr_count):
                        #print "[LK] [DEBUG] writting instruction in first block"
                        LK_LOG(0, "Escribiendo instrucciones en el primer bloque")
                        lk_sub_blk1.append(instr) 
                    elif(count == curr_instr_count):
                        #print "[LK] [DEBUG] Ending first block"
                        LK_LOG(0, "Finalizando primer bloque de codigo...")
                        lk_sub_blk1.append("                jmp     " + LK_LBL_BASE + str(block_count) + "\n")
                        lk_blck.append(lk_sub_blk1)
                        #print "[LK] [DEBUG] Initializing second block"
                        LK_LOG(0, "Inincializando segundo bloque de codigo...")
                        lk_sub_blk2.append(LK_LBL_BASE + str(block_count) + ":\n")
                        block_count+=1
                        lk_sub_blk2.append(instr)
                    else:
                        #print "[LK] [DEBUG] writting instruction in second block" 
                        LK_LOG(0, "Escribiendo instrucciones en el segundo bloque")
                        lk_sub_blk2.append(instr) 

                    count+=1
 
                #print "[LK] [DEBUG] Ending second block"
                #lk_blck.append(lk_sub_blk2)

                #print "[LK] [DEBUG] Second block --> block"
                LK_LOG(0, "Estableciendo segundo bloque para analisis...")
                block=lk_sub_blk2 

            else:
                #print "[LK] [DEBUG] Block is too short. Writting it and continuing..."
                LK_LOG(0, "El bloque es demasiado pequeno para ser dividido. Continuando...")
                lk_blck.append(block)
                split_block_ends=True
            
    
        curr_instr_count = random.randint(LK_MIN_INSTR, LK_MAX_INSTR)

    return lk_blck 

def correctIndivisible(blocks_section):
    lk_blck_tmp=blocks_section
    lk_blck=list()
    i = 0

    while i < len(lk_blck_tmp):
        LK_LOG(0, "Checking indivisible block...")
        LK_LOG(0, "\tChecking block " +  lk_blck_tmp[i][0] + " -> " + lk_blck_tmp[i][-2])
        must_correct=False
        if(len(lk_blck_tmp[i]) > 2):
            for instr_indv in LK_ASM_INSTR_INDV:
                if(checkLine(lk_blck_tmp[i][-2], instr_indv)):
                    LK_LOG(0, "Indivisible block")
                    if(checkLine(lk_blck_tmp[i][-1], LK_ASM_JMP)):
                        LK_LOG(0, "Must Correct")
                        must_correct=True
                        break;
        
            if(must_correct==True):
                LK_LOG(0, "Correcting...")
                lk_blck_union = lk_blck_tmp[i][:-1]  
                lk_blck_union.extend(lk_blck_tmp[i+1][1:])
                lk_blck.append(lk_blck_union)
                i+=1
            else:
                LK_LOG(0, "Block is ok")
                lk_blck.append(lk_blck_tmp[i])

        else:
            LK_LOG(0, "Block is short")
            lk_blck.append(lk_blck_tmp[i])

        i+=1

    return lk_blck


def usage():
    LK_LOG(3, "Parametros invalidos. Uso:\n\trnd_jmps.py -i <input_file> -o <output_file>")
    LK_EXIT(1)


####
# CONSTANTS
####
LK_SECTIONDELIMITER   = "section[\t ]*.*[\t ]*"
LK_SECTIONESTRACT     = "section[\t ]*(?P<section_name>.*)[\t ]*"
LK_HEADER_SEC         = "section[\t ]*UPX1HEAD[\t ]*"
LK_ASM_INSTR          = "[\t ]*.*[\t ]*.*"
LK_ASM_JMP            = "[\t ]*jmp[\t ]*.*"
LK_ASM_SECTION        = ".*:[\t ]*"
LK_BLANK_LINE         = "[\t\r\n ]*"

LK_MAX_INSTR          = 5 #Tamano maximo de bloque
LK_MIN_INSTR          = 3 #Tamano minimo de bloque

LK_LBL_BASE           = "lk_blk"

#LK_ASM_INSTR_INDV     = ["[\t ]*rep.*[\t ]*.*"]
LK_ASM_INSTR_INDV     = ["[\t ]*rep.*[\t ]*.*"]

section_pattern = re.compile(LK_SECTIONESTRACT)

####
# PARSING ARGUMENTS
####
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:v:l:')
except:
    #print "[LK] [ERROR] Invalid parameters. Usage:"
    #print "\trnd_jmps.py -i <input_file> -o <output_file> -c -r"
    usage()
    #LK_LOG(3, "Parametros invalidos. Uso:\trnd_jmps.py -i <input_file> -o <output_file>")
    #exit(1)

for opt, arg in opts:
    if opt == '-i':
        input_file = arg
    elif opt == '-o':
        output_file = arg
    elif opt == '-v':
        try:
            loglevel = int(arg)
        except:
            None
    elif opt == '-l':
        parts = arg.split(',')
        if(len(parts) == 2):
            LK_MIN_INSTR = int(parts[0])
            LK_MAX_INSTR = int(parts[1])
    else:
        usage()

if 'input_file' not in locals() or 'output_file' not in locals():
    usage()


####
# PROCESS
####
#print "[LK] [INFO] Starting chucu-chucu process..."
LK_LOG(1, "Iniciando proceso 'chucu-chucu'...")
LK_LOG(1, "Min: " + str(LK_MIN_INSTR) + " Max: " + str(LK_MAX_INSTR))

lk_input_stub     = open(input_file)
# Check if open
if lk_input_stub.closed:
    #print "[LK] [INFO] Can't open input file: " + input_file
    LK_LOG(3, "No se puede abrir el fichero de entrada: '" + input_file + "'. Saliendo...")
    LK_EXIT(1)


lk_output_stub    = open(output_file,'w+')
# Check if open
if lk_output_stub.closed:
    #print "[LK] [INFO] Can't open output file: " + output_file
    LK_LOG(3, "No se puede abrir el proceso de salida: '" + output_file + "'. Saliendo...")
    LK_EXIT(1)

lk_output_stub.close()

#print "[LK] [INFO] Searching for first section..."
#LK_LOG(1, "Buscando primera Seccion UPX...")
stub_structured   = {}
stub_order        = list()
current_section   = list()
section_name      = "HEADER"

stub_order.append(section_name)
#print "[LK ][INFO] Parsing stub..."
LK_LOG(1, "Iniciando el parseo del STUB UPX...")
line = lk_input_stub.readline()

LK_LOG(0, "Iniciando parseo de seccion: " + section_name)
while line:
    #print "[DEBUG] Line: " + line 
    LK_LOG(0, line[:-1])
    section_match = section_pattern.match(line)
    if(section_match == None):
        #print "[DEBUG] Instruction: " + line
        LK_LOG(0, "Es instruccion o etiqueta")
        current_section.append(line)
    else:
        #print "[DEBUG] New section found."
        LK_LOG(0, "Es seccion de UPX!")
        #print "[DEBUG] Closing las section: " + section_name
        LK_LOG(0, "Cerrando seccion: " + section_name)

        if section_name in stub_structured:
            #print "[LK] [WARNING] There are repeated section names!!"
            LK_LOG(2, "Existen secciones con nombres repetidos!")

        stub_structured[section_name] = current_section

        current_section = list()
        section_name = section_match.group("section_name")
        stub_order.append(section_name)
        #print "[DEBUG] Creating section: " + section_name  
        LK_LOG(0, "Iniciando parseo de seccion: " + section_name)

    line = lk_input_stub.readline()


stub_structured[section_name] = current_section

LK_LOG(1, "HECHO!")

stub_parsed = {}

#print "[LK] [INFO] Parsing codeblocks..."
LK_LOG(1, "Iniciando parseo secciones de UPX en bloques de codigo...")
for section_name in stub_order[1:-1]:
    stub_parsed[section_name] = parseSection(stub_structured[section_name])

#print "[LK] [INFO] Done!"
LK_LOG(1, "HECHO!")

#random.shuffle(stub_parsed[stub_order[1]])
#random.shuffle(stub_parsed[stub_order[2]])
#random.shuffle(stub_parsed[stub_order[3]])

# DEBUG WRITE FILE BY SECTIONS
#printSectionToFile(stub_structured[stub_order[0]], "/tmp/stub-reconstruction.txt", 'w+')
#printBlocksToFile(stub_order[1:-1], stub_parsed, "/tmp/stub-reconstruction.txt")
#fout = open("/tmp/stub-reconstruction.txt",'a+')
# Check if open
#if fout.closed:
#    print "[LK] [DEBUG] Can't open output file: " + "/tmp/stub-reconstruction.txt"
#    exit(1)
#fout.write("section         " + stub_order[-1] + "\n")
#fout.close()
#printSectionToFile(stub_structured[stub_order[-1]], "/tmp/stub-reconstruction.txt", 'a+')
#LK_LOG(1, "Escribiendo fichero de salida")
#printSectionToFile(stub_structured[stub_order[0]], output_file, 'w+')
#printBlocksToFile([stub_order[1]], stub_parsed, output_file)
#printBlocksToFile([stub_order[1]], stub_structured, output_file)
#printBlocksToFile([stub_order[2]], stub_parsed, output_file)
#printBlocksToFile([stub_order[2]], stub_structured, output_file)
#printBlocksToFile([stub_order[3]], stub_parsed, output_file)
#printBlocksToFile([stub_order[3]], stub_structured, output_file)
#fout = open(output_file,'a+')
#Check if open
#if fout.closed:
#    print "[LK] [DEBUG] Can't open output file: " + output_file
#    LK_EXIT(1)
#fout.write("section         " + stub_order[-1] + "\n")
#fout.close()
#printSectionToFile(stub_structured[stub_order[-1]], output_file, 'a+')
#LK_LOG(1, "HECHO!")
#
#LK_EXIT(0)



#### WRITE FILE
#LK_LOG(1, "Escribiendo fichero de salida")
#printSectionToFile(stub_structured[stub_order[0]], output_file, 'w+')
#printBlocksToFile(stub_order[1:-1], stub_parsed, output_file)
#fout = open(output_file,'a+')
# Check if open
#if fout.closed:
#    print "[LK] [DEBUG] Can't open output file: " + output_file
#    LK_EXIT(1)
#fout.write("section         " + stub_order[-1] + "\n")
#fout.close()
#printSectionToFile(stub_structured[stub_order[-1]], output_file, 'a+')
#LK_LOG(1, "HECHO!")

#LK_EXIT(0)


stub_codeblocks = {}
#print "[LK] [INFO] Parsing codeblocks..."
LK_LOG(1, "Iniciando subdivision de bloques de codigo...")
#for section_name in stub_order[1:-1]:
#    stub_codeblocks[section_name] = splitCodeblocks(stub_parsed[section_name])
#stub_codeblocks[stub_order[1]] = stub_parsed[stub_order[1]]
stub_codeblocks[stub_order[1]] = correctIndivisible(splitCodeblocks(stub_parsed[stub_order[1]]))
#stub_codeblocks[stub_order[2]] = stub_parsed[stub_order[2]]
stub_codeblocks[stub_order[2]] = correctIndivisible(splitCodeblocks(stub_parsed[stub_order[2]]))
#stub_codeblocks[stub_order[3]] = stub_parsed[stub_order[3]]
stub_codeblocks[stub_order[3]] = correctIndivisible(splitCodeblocks(stub_parsed[stub_order[3]]))

#print "[LK] [INFO] Done!"
LK_LOG(1, "HECHO!")

#LK_LOG(1, "Escribiendo fichero de salida")
#printSectionToFile(stub_structured[stub_order[0]], output_file, 'w+')
#printBlocksToFile(stub_order[1:-1], stub_codeblocks, output_file)
#fout = open(output_file,'a+')
## Check if open
#if fout.closed:
#    print "[LK] [DEBUG] Can't open output file: " + output_file
#    LK_EXIT(1)
#fout.write("section         " + stub_order[-1] + "\n")
#fout.close()
#printSectionToFile(stub_structured[stub_order[-1]], output_file, 'a+')
#LK_LOG(1, "HECHO!")
#
#LK_EXIT(0)

#stub_unordered = {}
LK_LOG(1, "Iniciando desordenado de bloques de codigo...")
#for section_name in stub_order[1:-1]:
#    #random.shuffle(stub_codeblocks[section_name])
#    stub_unordered[section_name] = stub_codeblocks[section_name].shuffle()

#print "[LK] [INFO] Done!"

#random.shuffle(stub_codeblocks[stub_order[1]])
random.shuffle(stub_codeblocks[stub_order[2]])
random.shuffle(stub_codeblocks[stub_order[3]])
LK_LOG(1, "HECHO!")

LK_LOG(1, "Escribiendo fichero de salida")
printSectionToFile(stub_structured[stub_order[0]], output_file, 'w+')
printBlocksToFile(stub_order[1:-1], stub_codeblocks, output_file)
fout = open(output_file,'a+')
# Check if open
if fout.closed:
    print "[LK] [DEBUG] Can't open output file: " + output_file
    LK_EXIT(1)
fout.write("section         " + stub_order[-1] + "\n")
fout.close()
printSectionToFile(stub_structured[stub_order[-1]], output_file, 'a+')
LK_LOG(1, "HECHO!")


LK_EXIT(0)
