# Template by Bruce A. Maxwell, 2015
#
# implements a simple assembler for the following assembly language
# 
# - One instruction or label per line.
#
# - Blank lines are ignored.
#
# - Comments start with a # as the first character and all subsequent
# - characters on the line are ignored.
#
# - Spaces delimit instruction elements.
#
# - A label ends with a colon and must be a single symbol on its own line.
#
# - A label can be any single continuous sequence of printable
# - characters; a colon or space terminates the symbol.
#
# - All immediate and address values are given in decimal.
#
# - Address values must be positive
#
# - Negative immediate values must have a preceeding '-' with no space
# - between it and the number.
#

# Language definition:
#
# LOAD D A   - load from address A to destination D
# LOADA D A  - load using the address register from address A + RE to destination D
# STORE S A  - store value in S to address A
# STOREA S A - store using the address register the value in S to address A + RE
# BRA L      - branch to label A
# BRAZ L     - branch to label A if the CR zero flag is set
# BRAN L     - branch to label L if the CR negative flag is set
# BRAO L     - branch to label L if the CR overflow flag is set
# BRAC L     - branch to label L if the CR carry flag is set
# CALL L     - call the routine at label L
# RETURN     - return from a routine
# HALT       - execute the halt/exit instruction
# PUSH S     - push source value S to the stack
# POP D      - pop form the stack and put in destination D
# OPORT S    - output to the global port from source S
# IPORT D    - input from the global port to destination D
# ADD A B C  - execute C <= A + B
# SUB A B C  - execute C <= A - B
# AND A B C  - execute C <= A and B  bitwise
# OR  A B C  - execute C <= A or B   bitwise
# XOR A B C  - execute C <= A xor B  bitwise
# SHIFTL A C - execute C <= A shift left by 1
# SHIFTR A C - execute C <= A shift right by 1
# ROTL A C   - execute C <= A rotate left by 1
# ROTR A C   - execute C <= A rotate right by 1
# MOVE A C   - execute C <= A where A is a source register
# MOVEI V C  - execute C <= value V
#

# 2-pass assembler
# pass 1: read through the instructions and put numbers on each instruction location
#         calculate the label values
#
# pass 2: read through the instructions and build the machine instructions
#

import sys

# converts d to an 8-bit 2-s complement binary value
def dec2comp8( d, linenum ):
    if(type(d) == type("string")): # Converting to int if needed
        d = int(d)

    try:
        if d > 0:
            l = d.bit_length()
            v = "00000000"
            v = v[0:8-l] + format( d, 'b')
        elif d < 0:
            dt = 128 + d
            l = dt.bit_length()
            v = "10000000"
            v = v[0:8-l] + format( dt, 'b')[:]
        else:
            v = "00000000"
    except:
        print('Invalid decimal number on line %d' % (linenum))
        exit()

    return v

# converts d to an 8-bit unsigned binary value
def dec2bin8( d, linenum ):
    if(type(d) == type("string")): # Converting to int if needed
        d = int(d)

    if d > 0:
        l = d.bit_length()
        v = "00000000"
        v = v[0:8-l] + format( d, 'b' )
    elif d == 0:
        v = "00000000"
    else:
        print('Invalid address on line %d: value is negative' % (linenum))
        exit()

    return v


# Tokenizes the input data, discarding white space and comments
# returns the tokens as a list of lists, one list for each line.
#
# The tokenizer also converts each character to lower case.
def tokenize( fp ):
    tokens = []

    # start of the file
    fp.seek(0)

    lines = fp.readlines()

    # strip white space and comments from each line
    for line in lines:
        ls = line.strip()
        uls = ''
        for c in ls:
            if c != '#':
                uls = uls + c
            else:
                break

        # skip blank lines
        if len(uls) == 0:
            continue

        # split on white space
        words = uls.split()

        newwords = []
        for word in words:
            newwords.append( word.lower() )

        tokens.append( newwords )

    return tokens

# Takes in a table and register name and returns the corresponding 3 bit
# binary value representation for that table
def getRegisterValue(regName, tableName,line_num=None):
    regName = str.lower(regName)
    tableName = str.lower(tableName)
    returnvalue = None
    if tableName == "b":
        options = { "ra" : "000",
                    "rb" : "001",
                    "rc" : "010",
                    "rd" : "011",
                    "re" : "100",
                    "sp" : "101",
                    }
        returnvalue = options.get(regName)
    elif tableName == "c":
        options = { "ra" : "000",
            "rb" : "001",
            "rc" : "010",
            "rd" : "011",
            "re" : "100",
            "sp" : "101",
            "pc" : "110",
            "cr" : "111",
        }
        returnvalue = options.get(regName)
    elif tableName == "d":
        options = { "ra" : "000",
            "rb" : "001",
            "rc" : "010",
            "rd" : "011",
            "re" : "100",
            "sp" : "101",
            "pc" : "110",
            "ir" : "111",
        }
        returnvalue = options.get(regName)
    elif tableName == "e":
        options = { "ra" : "000",
            "rb" : "001",
            "rc" : "010",
            "rd" : "011",
            "re" : "100",
            "sp" : "101",
            "zeros" : "110",
            "ones" : "111",
        }
        returnvalue = options.get(regName)
    else:
        print(f"ERROR - Line {line_num} - Table {tableName} not found")
        exit()

    if(returnvalue == None):
        print(f"ERROR - Line {line_num} - Register {regName} not found for table {tableName}")
        exit()
        
    return returnvalue


# reads through the file and returns a dictionary of all location
# labels with their line numbers
# Label is a basically being treated as a "function" name, e.g. loop:
def pass1( tokens ):
    label_dict = {}
    line_num = 0
    for line in tokens:
        label = line[0]
        if label[-1] == ':': # if the current line is a valid label
            label = label[:-1]
            if (not(label_dict.__contains__(label))): # If current label is not already in dict
                label_dict[label] = line_num # Currently is removing the :
                del tokens[line_num] # Removing the label from the list
            else: # If label is already present
                print(f"ERROR - Line {line_num} - The label {label} occurs more than once")
                exit()
        line_num += 1

    return label_dict, tokens

# Reads over the tokens and generates binary machine instructions from them
def pass2( label_dict, tokens ):
    bin_instructs = []
    line_num = 0
    for line in tokens:
        instr = line[0] # Getting the instruction type
        cur_bin_instruct = None # Initializing an opcode variable
        
        # Checking for bad label names
        if("bra" in instr and label_dict.get(line[1]) == None):
            print(f"ERROR - Line {line_num} - No label {line[1]} found. \nTry one of: {label_dict.keys()}")
            exit()
        # Big If/else if block for each instruction type
        if instr == "load":
            cur_bin_instruct = "0000" + "0" # this second 0 is the R bit
            cur_bin_instruct += getRegisterValue(line[1],"b",line_num) + dec2bin8(line[2], line_num)
        elif instr == "loada":
            cur_bin_instruct = "0000" + "1" # this second 0 is the R bit
            cur_bin_instruct += getRegisterValue(line[1],"b",line_num) + dec2bin8(line[2], line_num)  
        elif instr == "store":
            cur_bin_instruct = "0001" + "0" # this second 0 is the R bit
            cur_bin_instruct += getRegisterValue(line[1],"b",line_num) + dec2bin8(line[2], line_num)
        elif instr == "storea":
            cur_bin_instruct = "0001" + "1" # this second 0 is the R bit
            cur_bin_instruct += getRegisterValue(line[1],"b",line_num) + dec2bin8(line[2], line_num) 
        elif instr == "bra":
            cur_bin_instruct = "0010" + "0000" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "braz": 
            cur_bin_instruct = "0011" + "00" + "00" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "bran": 
            cur_bin_instruct = "0011" + "00" + "10" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "brao": 
            cur_bin_instruct = "0011" + "00" + "01" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "brac": 
            cur_bin_instruct = "0011" + "00" + "11" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "call": 
            cur_bin_instruct = "0011" + "01" + "00" + dec2bin8(label_dict[line[1]], line_num)
        elif instr == "return": 
            cur_bin_instruct = "0011" + "10" + "00" + "00000000"
        elif instr == "halt": 
            print("ERROR: Instruction HALT not implemented on CPU")
            cur_bin_instruct = "0011" + "11" + "00" + "00000000"
        elif instr == "push":
            cur_bin_instruct = "0100" + getRegisterValue(line[1],'c',line_num) + "000000000"      
        elif instr == "pop":
            cur_bin_instruct = "0101" + getRegisterValue(line[1],'c',line_num) + "000000000" 
        elif instr == "oport":
            cur_bin_instruct = "0110" + getRegisterValue(line[1],'d',line_num) + "000000000"
        elif instr == "iport":
            cur_bin_instruct = "0111" + getRegisterValue(line[1],'b',line_num) + "000000000"
        elif instr == "add":
            cur_bin_instruct = "1000" + getRegisterValue(line[1],'e',line_num)  
            cur_bin_instruct += getRegisterValue(line[2],'e',line_num) + "000"
            cur_bin_instruct += getRegisterValue(line[3],'b',line_num)
        elif instr == "sub":
            cur_bin_instruct = "1001" + getRegisterValue(line[1],'e',line_num)  
            cur_bin_instruct += getRegisterValue(line[2],'e',line_num) + "000"
            cur_bin_instruct += getRegisterValue(line[3],'b',line_num)
        elif instr == "and":
            cur_bin_instruct = "1010" + getRegisterValue(line[1],'e',line_num)  
            cur_bin_instruct += getRegisterValue(line[2],'e',line_num) + "000"
            cur_bin_instruct += getRegisterValue(line[3],'b',line_num)
        elif instr == "or":
            cur_bin_instruct = "1011" + getRegisterValue(line[1],'e',line_num)  
            cur_bin_instruct += getRegisterValue(line[2],'e',line_num) + "000"
            cur_bin_instruct += getRegisterValue(line[3],'b',line_num)
        elif instr == "xor":
            cur_bin_instruct = "1100" + getRegisterValue(line[1],'e',line_num)  
            cur_bin_instruct += getRegisterValue(line[2],'e',line_num) + "000"
            cur_bin_instruct += getRegisterValue(line[3],'b',line_num)
        elif instr == "shiftl":
            cur_bin_instruct = "1101" + "0" + getRegisterValue(line[1],'e',line_num) + "00000" 
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        elif instr == "shiftr":
            cur_bin_instruct = "1101" + "1" + getRegisterValue(line[1],'e',line_num) + "00000" 
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        elif instr == "rotl":
            cur_bin_instruct = "1110" + "0" + getRegisterValue(line[1],'e',line_num) + "00000" 
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        elif instr == "rotr":
            cur_bin_instruct = "1110" + "1" + getRegisterValue(line[1],'e',line_num) + "00000" 
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        elif instr == "move":
            cur_bin_instruct = "1111" + "0" + getRegisterValue(line[1],'d',line_num) + "00000" 
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        elif instr == "movei":
            cur_bin_instruct = "1111" + "1" + dec2bin8(line[1], line_num)
            cur_bin_instruct += getRegisterValue(line[2],'b',line_num)
        else:
            print(f"ERROR - Line {line_num} - No such Instruction: {instr} ")
            exit()
                                           
        bin_instructs.append(cur_bin_instruct)
        line_num += 1

    return bin_instructs

# Creates the MIF file from the list of binary instructions
def createMIF(bin_instructs, filename):
    fp = open(filename, 'w')
    fp.write(f"-- Program Memory file for {filename}\n")
    fp.write("DEPTH = 256;\n")
    fp.write("WIDTH = 16;\n")
    fp.write("ADDRESS_RADIX = HEX;\n")
    fp.write("DATA_RADIX = BIN;\n")
    fp.write("CONTENT\n")
    fp.write("BEGIN\n")
    
    for i in range(len(bin_instructs)):
        if(i < 16):
            hexval = hex(i) + ""
            hexval = "0" + hexval[2:] 
        else:
            hexval = (hex(i)+"")[2:]
        hexval = hexval.upper()

        fp.write(f"{hexval} : {bin_instructs[i]};\n")

    if(i+1 < 16):
        hexval = hex(i+1) + ""
        hexval = "0" + hexval[2:] 
    else:
        hexval = (hex(i+1)+"")[2:]
    hexval = hexval.upper()
    

    fp.write(f"[{hexval}..FF] : 1111111111111111;\nEND")

    return

def main( argv ):
    if len(argv) < 3:
        print('Usage: python %s <input filename> <output.mif filename>' % (argv[0]))
        exit()

    fp = open( argv[1], 'r')

    tokens = tokenize( fp )
    # print(tokens,"\n","\n")

    fp.close()

    # execute pass1 and pass2 then print it out as an MIF file
    label_dict, tokens = pass1(tokens)
    
    bin_instructs = pass2(label_dict, tokens)
    

    createMIF(bin_instructs, argv[2])

    return


if __name__ == "__main__":
    main(sys.argv)
    