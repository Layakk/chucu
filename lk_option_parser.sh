#!/bin/bash
########################
## lk_option_parser.sh
##	Library module of bash functions to parse program options
##
## Copyright (C) 2014 LAYAKK - www.layakk.com
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## COMMENTS:
##	(*) We don't distinguish between option and argument, so every option
##	must be passed as a flagged argument, which may or maynot be mandatory.
##	(*) When a default value for a function parameter is defined, it is 
##	assigned when the parameter is not passed or is "".
## USAGE:
## 	To use the functions defined in this code, source this file in your 
## 	program using ". lk_option_parser.sh || exit 1". 
##	lk_option_parser.sh can be in the same directory of your program, 
##	in a directory accesible by your environment PATH variable or you can 
##	also specify a full path for lk_option_parser.sh.
##
##	The following functions have been defined for use in your code:
##	add_program_option
##		Use this function to add a program option to your bash program 
##		(see parameters below). You should use this function (once for 
##		each parameter you want to use before doing anything else.
##	parse_program_options	
##		Use "parse_program_options $@" immediately after the last 
##		call to add_program_option.
##	show_program_usage
##		Shows program usage. If you invoke it without arguments it 
##		just run, but if a short option is passed as an argument, then
##		it only runs if the option is specified. It returns 0 when it
##		has run, so tipical invocation is: 
##			'show_program_usage "-h" && exit 0'
##	is_option_present
##		Returns 0 if the short flag passed as argument is present in 
##		the command line.
##	get_option_value
##		Returns an option value on standar output. The value associated to
##		the option is everything between the option flag and the next 
##		short or long option flag, or the end of the command line.
##		Typically invoke this function as var=`get_option_value "-f"`. 
##		It does not check whether the option is present or not 
##		(if the option is not present an empty string is returned).
########################
# INITIALIZATION
tabs -8 >/dev/null 2>&1

# GLOBAL VARIABLS SECTION
unset _OPTION_LONG_FLAG
unset _OPTION_DESCRIPTION
unset _OPTION_IS_MANDATORY
unset _OPTION_REQUIRES_ARG
unset _OPTION_VALUE
unset _OPTION_FLAG_IS_PRESENT
unset _REQ_VALUE
unset _PROGRAM_NAME
typeset -A _OPTION_LONG_FLAG
typeset -A _OPTION_DESCRIPTION
typeset -A _OPTION_IS_MANDATORY
typeset -A _OPTION_REQUIRES_ARG
typeset -A _OPTION_VALUE
typeset -A _OPTION_FLAG_IS_PRESENT
typeset -a _REQ_VALUE
typeset _PROGRAM_NAME=$0

# FUNCTION SECTION
# ... add_program_option ...
# $1 is the short flag		("-c" where c is a character | no default value)
# $2 is the long flag 		("--word" | default="")
# $3 is the description		("option description" | default="")
# $4 is the mandatory flag	("{YES|NO}" | default="NO")
# $5 requires argument  	("{YES|NO}" | default="NO")
# ...
function add_program_option {
	_short_flag=${1:?"function add_programa_option takes at least one parameter! Exiting."}
	if [[ ! "$_short_flag" =~ ^[-]{1}[[:alnum:]]{1}$ ]]
	then
		printf "Illegal short flag: '$_short_flag' ! Exiting.\n"
		exit 1
	fi
	_long_flag=$2
	if [[ ! "$_long_flag" =~ ^[-]{2}[[:alnum:]-]+$ ]]
	then
		printf "Illegal long flag $_long_flag. Exiting\n"
		exit 1
	fi
	_OPTION_LONG_FLAG["$_short_flag"]=$_long_flag
	_OPTION_FLAG_IS_PRESENT["$_short_flag"]="NO"
	if [[ ${#3} -eq 0 ]]
	then
		_OPTION_DESCRIPTION["$_short_flag"]=""
	else
		_OPTION_DESCRIPTION["$_short_flag"]=$3
	fi
	if [[ ${#4} -eq 0 ]]
	then
		_OPTION_IS_MANDATORY["$_short_flag"]="NO"
	else
		if [[ $4 == "YES" || $4 == "NO" ]]
		then
			_OPTION_IS_MANDATORY["$_short_flag"]=$4
		else
			printf "mandatory flag '$4' is not correct. Correct values are 'YES' and 'NO'. Exiting.\n"
			exit 1
		fi
	fi
	if [[ ${#5} -eq 0 ]]
	then
		_OPTION_REQUIRES_ARG["$_short_flag"]="NO"
	else
		if [[ $5 == "YES" || $5 == "NO" ]]
		then	
			_OPTION_REQUIRES_ARG["$_short_flag"]=$5
		else
			printf "requires arg flag '$5' is not correct. Correct values are 'YES' and 'NO'. Exiting.\n"
			exit 1
		fi
	fi
}

# ... parse_program_options ...
# ... always pass $@ as argument
function parse_program_options {
typeset -i arg_index
typeset -i req_value_index
typeset -i wordcount

	arg_index=1
	req_value_index=0

	# Get all options and its values
	while [[ $arg_index -le $# ]]
	do
		if [[ "${!_OPTION_LONG_FLAG[*]}" =~ ${!arg_index} ]]
		then
			_short_flag=${!arg_index}
			_OPTION_FLAG_IS_PRESENT["$_short_flag"]="YES"
		else 
			_short_flag=""
			for _key in ${!_OPTION_LONG_FLAG[*]}
			do
				if [[ ${_OPTION_LONG_FLAG[$_key]} == ${!arg_index} ]]
				then
					_short_flag=$_key
					break
				fi
			done
			if [[ ${#_short_flag} -eq 0 ]] 
			then
				printf "Unrecognized option '${!arg_index}'. Exiting. \n\n"
				show_program_usage
				exit 1
			fi
			_OPTION_FLAG_IS_PRESENT[$_short_flag]="YES"
		fi
		_long_flag=_${_OPTION_LONG_FLAG[$_short_flag]}
		if [[ ${_OPTION_REQUIRES_ARG[$_short_flag]} == "YES" ]]
		then
			arg_index=arg_index+1
			if [[ $arg_index -gt $# || ${!arg_index}  =~ ^[-]{1}[[:alnum:]]{1}$ || ${!arg_index} =~ ^[-]{2}[[:alnum:]]+$ ]]
			then
				printf "Required value for option '$_short_flag' is not present! Exiting.\n\n"
				show_program_usage
				exit 1
			else
				_OPTION_VALUE[$_short_flag]=""
				wordcount=0
				while [[ ! ${!arg_index} =~ ^[-]+.* && $arg_index -le $# ]]
				do
					if [[ $wordcount -eq 0 ]]
					then
						_OPTION_VALUE[$_short_flag]=${!arg_index}
					else
						_OPTION_VALUE[$_short_flag]=${_OPTION_VALUE[$_short_flag]}" "${!arg_index}
					fi
					arg_index=arg_index+1
					wordcount=wordcount+1
				done
			fi
		else
				arg_index=arg_index+1
		fi
	done

	# Check presence of required options
	for _short_flag in ${!_OPTION_LONG_FLAG[@]}
	do
		if [[ ${_OPTION_FLAG_IS_PRESENT[$_short_flag]} != "YES" && ${_OPTION_IS_MANDATORY[$_short_flag]} == "YES" ]]
		then
			printf "Mandatory flag '$_short_flag' is not present! Exiting.\n\n"
			show_program_usage
			exit 1
		fi
	done
}

#... is_option_present ...
#... $1 must be a short flag (in the form of "-f")
function is_option_present {
	[[ ${#1} -eq 0 ]] && return 1
	[[ ${_OPTION_FLAG_IS_PRESENT[$1]} == "YES" ]] && return 0
	return 1
}

##... get_option_value ...
#... $1 must be a short flag (in the form of "-f")
function get_option_value {
	[[ ${#1} -eq 0 ]] && return 1
	echo ${_OPTION_VALUE[$1]}
}

#... show_program_usage
#...
function show_program_usage {
typeset -i ncols
typeset -i current_index

	if [[ "$1" =~ ^[-]{1}[[:alnum:]]{1}$ ]]
	then
		if ! is_option_present "$1" 
		then
			return 1
		fi
	fi
	
	printf "Usage:\n"
	printf "\t$0"
	for _short_flag in ${!_OPTION_LONG_FLAG[@]}
	do
		string="${_short_flag}|${_OPTION_LONG_FLAG[$_short_flag]}"
		if [[ ${_OPTION_REQUIRES_ARG[$_short_flag]} == "YES" ]]
		then
			string=$string" option"
		fi
		if [[ ${_OPTION_IS_MANDATORY[$_short_flag]} != "YES" ]]
		then
			string=" [ "$string" ]"
		else
			string=" "$string
		fi
		printf "$string"
	done
	printf "\n"

	for _short_flag in ${!_OPTION_LONG_FLAG[@]}
	do
		printf "\t\t${_short_flag}|${_OPTION_LONG_FLAG[$_short_flag]} :\n"
		ncols=`tput cols`-25
		if [[ ncols -lt 0 ]]
		then
			printf "\nPlease reize your terminal!Exiting.\n\n"
			exit 1
		fi
		current_index=0
		description=${_OPTION_DESCRIPTION[$_short_flag]}
		while [[ $current_index -lt ${#description} ]]
		do
			thisline=${description:current_index:ncols}
			printf "\t\t\t$thisline\n"
			current_index=current_index+ncols
		done
	done
	
	return 0
}
