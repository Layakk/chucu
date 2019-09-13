#!/usr/bin/python
import re
import random
import sys

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
def checkLine(line, LK_PATTERN):
    match = re.match(LK_PATTERN, line)
    if(match == None):
        return False

    return True

def writeArrayIntoFile(file_out, array):
    for instr_line in array:
        file_out.write(instr_line)

####
# CONSTANTS
####
LK_SECTIONDELIMITER   = "section[\t ]*.*[\t ]*"
LK_SECTIONESTRACT   = "section[\t ]*(?P<section_name>.*)[\t ]*"
LK_LISTITEMS   = "\[LK\][\t ]*\[LIST\][\t ]*(?P<section_name>.*)"
LK_LISTSTART   = "\[LK\][\t ]*\[LIST\][\t ]*INIT"
LK_LISTEND     = "\[LK\][\t ]*\[LIST\][\t ]*END"

section_pattern = re.compile(LK_SECTIONESTRACT)
listitems_pattern = re.compile(LK_LISTITEMS)

####
# PARSING ARGUMENTS
####
if len(sys.argv) !=4:
    #print "[ERROR] Invalid number of arguments. Usage:"
    #print "\tlk_build_lkstub.py <input_stub> <output_stub> <label_lists>"
    LK_LOG(3, "Invalid number of arguments. Usage:\n\tlk_build_lkstub.py <input_stub> <output_stub> <label_lists>")
    LK_EXIT(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
list_file = sys.argv[3]

#input_file = "/home/chucu/Desktop/chucu_test/chucu/upx-3.91-src/src/stub/src/i386-win32.pe.S"
#output_file = "/home/chucu/Desktop/chucu_test/chucu/i386-win32.pe.S.MANUAL"
#list_file = "/home/chucu/Desktop/chucu_test/chucu/list_stub.txt"
####
# PROCESS
####
#print "[INFO] Starting chucu-chucu process..."
LK_LOG(1,"Starting building Custom Stub process...")

lk_input_stub     = open(input_file)

stub_structured   = {}
current_section   = list()
section_name      = "HEADER"

#print "[INFO] Parsing stub..."
LK_LOG(1, "Parsing stub...")
line = lk_input_stub.readline()
while line:
    #print "[DEBUG] Line: " + line 
    LK_LOG(0, "Line: " + line)
    section_match = section_pattern.match(line)
    if(section_match == None):
        #print "[DEBUG] Instruction: " + line
        LK_LOG(0, "Instruction: " + line)
        current_section.append(line)
    else:
        #print "[DEBUG] New section found."
        LK_LOG(0, "New section found.")
        #print "[DEBUG] Closing las section: " + section_name
        LK_LOG(0, "Closing las section: " + section_name)

        if section_name in stub_structured:
            #print "[WARNING] There are repeated section names!!"
            LK_LOG(2, "There are repeated section names!!")

        stub_structured[section_name] = current_section
        
        current_section = list()
        section_name = section_match.group("section_name")
        #print "[DEBUG] Creating section: " + section_name  
        LK_LOG(0, "Creating section: " + section_name)

    line = lk_input_stub.readline()


stub_structured[section_name] = current_section
#print "[INFO] Done!" 
LK_LOG(1, "Done!")

lk_input_list     = open(list_file)
lk_output_stub    = open(output_file,'w+')
#print "[INFO] Finding list start..."
LK_LOG(0, "Finding list start...")
line = lk_input_list.readline()
while line and not checkLine(line, LK_LISTSTART):
    #print "[DEBUG] Start not found: " + line
    LK_LOG(0, "Start not found: " + line)
    line = lk_input_list.readline()

#print "[DEBUG] Found! " + line
LK_LOG(0, "Found! " + line)
LK_LOG(0, "Done!")

LK_LOG(1, "Building lkstub...")
count = 0
#write head
writeArrayIntoFile(lk_output_stub, stub_structured["HEADER"]);

lk_output_stub.write("section         LKSTUB" + str(count) + "\n")
count = count +1

line = lk_input_list.readline()
while line and not checkLine(line, LK_LISTEND):
    list_match = listitems_pattern.match(line)
    if(list_match == None):
        #print "[WARNING] Not matching LK LIST line..."
        LK_LOG(2, "Not matching LK LIST line...")
        None
    else:
        list_item = list_match.group("section_name")
        #print "[DEBUG] Adding section: " + list_item
        LK_LOG(0, "Adding section: " + list_item)
        if(list_item == "*UND*"):
            #print "[DEBUG] Is *UND*"
            LK_LOG(0, "Is *UND*")
            None
        elif(list_item == "IDENTSTR"):
            #print "[DEBUG] Is IDENTSTR"
            LK_LOG(0, "Is IDENTSTR")
            None
        elif(list_item == "UPX1HEAD"):
            #print "[DEBUG] Is UPX1HEAD"
            LK_LOG(0, "Is UPX1HEAD")
            #Write "section UPX1HEAD".
            lk_output_stub.write("section         UPX1HEAD")
            #Then, write content of section.
            writeArrayIntoFile(lk_output_stub, stub_structured[list_item]);
        elif(list_item[0] == "+"):
            #print "[DEBUG] Is ALIGMENT"
            LK_LOG(0, "Is ALIGMENT")
            #Write new "section LKSECTIONX".
            lk_output_stub.write("section         LKSTUB" + str(count) + "\n")
            count = count +1
        else:
            LK_LOG(0, "Is Common Section")
            #Write content.
            writeArrayIntoFile(lk_output_stub, stub_structured[list_item]);
         
    line = lk_input_list.readline()

LK_LOG(1, "Done!")
