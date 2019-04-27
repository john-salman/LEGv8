import sys

###########################################################################################################################################
# Program: main.py
# Authors: John Salman, Tim Gallagher
# Description: This program allows user's to simulate execution of a LEGv8 program. Both in a standard full-through execution, and in a
#              a step-by-step psuedo debugger form. This application is intnended as an instructional tool and is thusly verbose when
#              being used in debugger (step) mode.
###########################################################################################################################################




###################################TO DO############################################
#          - parse and input B-Format, CB-Format
#          - take in program as input file, take in user-specified memory as input file (or command line input)
#          - continue to implement executions of all instructions
#          - handle overflow errors as interpreted events
#          - write logic to print specific registers
#          - change output forms from decimal to binary/hex, or back to decimal from binary to hex
#                   + we dont need to write a binary to hex functions, we can do binary -> decimal -> hex




##################################################################################                                                                                                                        
# Class: Control                                                                                                                                                                                            
# Description: This class is used as an interface to the Instructions class
#              and is used to navigate the application
##################################################################################
class Control:

    ##################################################################################
    # Function: _init_
    # Parameters: The file containing the LEGv8 program, user specified memory.
    # Description: This constructor method creates an instance of the instructions
    #              subclass. 
    ##################################################################################
    def __init__(self, fileName, MEM):
        self.instructions = Instructions(fileName, MEM)

    ##################################################################################
    # Function: step
    # Parameters: none
    # Description: This function acts as the primary user interface. It takes
    #              commands from the user, and responds as specified by the help
    #              command.
    ##################################################################################
    def step(self):
        print("Please enter a command at the prompt below (enter 'h' or 'help' for help)" )
        command = ""
        print self.instructions.program
        _next = self.instructions.str_current()
        while(_next != 'END'):
            print " "
            print "Current Line: " + self.instructions.str_current()
            command = raw_input("[LEGv8]: ")
            if (command == 'n' or command == 'next'):
                _next = self.instructions.execute()

            elif(command == 'p' or command == 'print'):
                self.instructions.print_all()

            elif (command[0:1] == 'p' and len(command) > 1 and command[1:2] != 'r'):
                self.instructions.print_specific(command)

            elif (command == 'h' or command == 'help'):
                print("This program supports the following arguements:                                               ")
                print("                                                                                              ")
                print("    p(rint)     - Can be used with or without arguements to print the values of an instruction")
                print("                  Without arguements, the command will print all relevant information of an   ")
                print("                  instruction. With arugements, the command will print the information of a   ")
                print("                  register, instrution name, memory value, or constant.                       ")
                print("                                                                                              ")
                print("                  Example:                                                                    ")
                print("                        p X11  =>  Register Value: 11                                         ")
                print("                                   Register Contents: 43                                      ")
                print("                                                                                              ")
                print("    n(ext)      - Is used to move to the next instruction and execute the current. Command is ")
                print("                  verbose so it will talk through the steps of execution.                     ")
                print("                                                                                              ")
                print("                  Example:                                                                    ")
                print("                        n  => Executing Line: ADDI X3, X4, #14                                ")
                print("                              Value of Write Register before execution: 4                     ")
                print("                              Evaluating interpreted expression: 8 + 14                       ")
                print("                              Value of Write Register after execution: 20                     ")
                print("                                                                                              ")
                print("                              New Line: CBZ X3, LABEL                                         ")
                print("                                                                                              ")
                print("    exit        - Is used to exit the current instance of this program.                       ")
                print("                                                                                              ")
                print("    decimal     - Is used to set print outputs to decimal.                                    ")
                print("                                                                                              ")
                print("    hex         - Is used to set print outputs to hexadecimal.                                ")
                print("                                                                                              ")
                print("    binary      - Is used to set print outputs to binary.                                     ")
                print("                                                                                              ")

            elif(command == 'e' or command == 'exit'):
                print("Exiting program...") # does python handles garbage collection right?
                print("Goodbye!")
                sys.exit(0)
                
            else:
                print("Command not recognized, please enter 'help' for a full list of commands.")
        print "User Program complete, exiting..."
        print "Goodbye!"
        return

    ##################################################################################
    # Function: full
    # Parameters: none
    # Description: This function is used to run the program without halting at any
    #              step.
    ##################################################################################
    def full(self):
        _next = self.instructions.str_current()
        while (_next != 'END'):
            _next = self.instructions.execute()
        return

##################################################################################
# Class: Instructions
# Description: This class interprets the user's program, it turns the line into 
#              objects that can be executed and analyzed by the user.
##################################################################################
class Instructions: 

    ##################################################################################
    # Function: _init_
    # Parameters: the file containing the user program, and user specified memory
    # Description: This function instantiates private variables and then calls a
    #              function to parse the file.
    ##################################################################################
    def __init__(self, fileName, _MEM):
        self.current_line = 0
        self.MEM = _MEM # set to dummy value for now
        self.flags = { # should be all the necessary flags, may need to implement pseudo-control-signals
            'Z': 0,
            'N': 0,
            'V': 0,
            'C': 0,
        }
        self.RFILE = [7, 5, -2, 6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.program = []

        # Place the name-value pairs in their appropriate spots as you go
        # NOTE: some opcodes may be incorrect depending on source material
        
        #I-Format
        #"ORRI": 1424,                                                             
        #"EORI": 1680,
        #"ADDIS": 1936,                                                             
        #"SUBIS": 1928,                                                                     
        #"ANDI": 1168,                                                                     
        #"ANDIS": ,                                                                     

        # B-Format                                                       
        #"B": 160,                                                                      
        #"BL": 1184,
        
        # D-Format
        #"STUR": 1984,     
        # LDUR
        #"STURH": 448,                                                                      
        #"LDURH": 450,      

        # R-Format
        #AND
        #"ANDS": 1104,                                                                     
        #"ADDS": 1368,                                                                     
        #"SUBS": 1880,                                                                     
        #"ORR": 1360,                                                                     
        #"EOR": 1616,                                                                     
        #"LSR": 1690,                                                                     
        #"LSL": 1691,                                                                     
        #"BR": 1712,
        
        # CB-Format
        #"CBZ": 1440,                                                                     
        #"CBNZ": 1448,      

        # This object has three primary purposes:
        # 1. Is used to determine the format type of an instruction
        # 2. Obtain opcode value of instruction
        # 3. Labels can be determined by their exclusion from this set
        self.instr_def = {
            'I-Format': {
                'ADDI': 1160,
                "SUBI": 1672,
            },
            'D-Format':{
                'STUR': 1984,
                'LDUR': 1986,
            },
            'R-Format': {
                'ADD': 1112,
                "SUB": 1624,
            }
        }
        self.Process_File(fileName)

    ##################################################################################
    # Function: Process_File
    # Parameters: the input file containing the user's program
    # Description: This function parses the file line by line, determining the format
    #              type, and operating under the pretense that if it's not an
    #              instruction then it is a label. Helper functions do perform some
    #              lexical validation, but not vary in-depth (Dr. Ravi stated all
    #              input will be valid).
    ##################################################################################
    def Process_File(self, fileName):
        with open(fileName) as file:
            lines = file.readlines()
        lineCount = 0
        current = ""
        i = 0
        while(lineCount < len(lines)):
            line = lines[lineCount]
            while(line[i] != " "):
                current += line[i]
                i += 1

            if (current in self.instr_def['I-Format']):
                self.Process_I_Format(line, i, current)
            elif (current in self.instr_def['R-Format']):
                self.Process_R_Format(line, i, current)
            elif (current in self.instr_def['D-Format']):
                self.Process_D_Format(line, i, current)
            else:
                print "Label detected"
            lineCount += 1
            current = ""
            i = 0
        return


    ##################################################################################
    # Function: Process_I_Format
    # Parameters: the line, index(may not be necessary if we trim the string in
    #             parent function), and current (aka the instruction name)
    # Description: This function parses the current line of the input file, seperating
    #              the values into an object interpretation
    ##################################################################################
    def Process_I_Format(self, line, i, current):
        instr = current # log the current as the instruction                                                                                 
        current = ""
        i += 1 # get off space                                                                                                                       
        if (line[i] == "X"): # Write register
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()
                
        while(line[i] != ","): # these loops append the digits into a temp variable
            current += line[i]
            i += 1

        rd_num = current
        current = ""
        i += 1 # get off comma                                                                                                                       
        i += 1 # get off space                                                                                                                       

        if (line[i] == "X"): # Rn
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()
            
            
        while(line[i] != ","):
            current += line[i]
            i += 1
            
        rn_num = current
        current = ""
        i += 1 # get off comma                                                                                                                       
        i += 1 # get off space                                                                                                                       

        if (line[i] == "#"): #immediate value
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit() # we should explore a more graceful bomb out
            
        while(i < len(line)):
            current += line[i]
            i += 1

        imm = current
        opcode = self.instr_def['I-Format'][instr]
        self.Make_I_Format(instr, opcode, imm, rn_num, rd_num) # insert new object in instruction array with line serving as index      
        return

    ##################################################################################
    # Function: Make_I_Format
    # Parameters: the parsed values provided by the parent function
    # Description: This function sorts the parameters and molds them into a more usable
    #              object format. This format makes actual instruction implementations
    #              more trivial.
    ##################################################################################
    def Make_I_Format(self, _name, _opcode, _imm, _rn, _rd):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'imm': int(_imm), 'Rn': int(_rn), 'Rd': int(_rd)}})
        return

    ##################################################################################               
    # Function: Process_D_Format                                                                                                              
    # Parameters: the line, index(may not be necessary if we trim the string in                                                                                             
    #             parent function), and current (aka the instruction name)           
    # Description: This function parses the current line of the input file, seperating
    #              the values into an object interpretation
    ##################################################################################
    def Process_D_Format(self, line, i, current):
        instr = current # log the current as the instruction                                                                                                                                                                 
        current = ""
        i += 1 # get off space
        
        if (line[i] == "X"): # Destination register                                                                                                            
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()

        while(line[i] != ","): # these loops append the digits into a temp variable                                                                                                                                                   
            current += line[i]
            i += 1

        rt_num = current
        current = ""
        i += 1 # get off comma                                                                                                                                                                                                            
        i += 1 # get off space

        if (line[i] == "["): # Start of addressing space
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()
            
        if (line[i] == "X"): # Rn
            i += 1
        else:
            print("Error: malformed instruction")
            sys.exit()


        while(line[i] != ","):
            current += line[i]
            i += 1

        rn_num = current
        current = ""
	i += 1 # get off comma                                                                                                                                                                            
        i += 1 # get off space

        if (line[i] == "#"): #addressing value
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit() # we should explore a more graceful bomb out
            
        while(i < len(line) and line[i] != ']' and line[i] != ' '):
            current += line[i]
            i += 1
            
        if (line[i] == "]"): # Rn                                                                                                                                             
	    i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()
        address = current
        opcode = self.instr_def['D-Format'][instr]
        self.Make_D_Format(instr, opcode, address, rn_num, rt_num) # insert new object in instruction array with line serving as index
        return

    ##################################################################################                                                                                 
    # Function: Make_D_Format
    # Parameters: the parsed values provided by the parent function
    # Description: This function sorts the parameters and molds them into a more usable                                                                  
    #              object format. This format makes actual instruction implementations
    #              more trivial.
    ##################################################################################                                                                                                              
    def Make_D_Format(self, _name, _opcode, _addr, _rn, _rt):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'address': int(_addr), 'Rn': int(_rn), 'Rt': int(_rt)}})
        return


    ################################################################################## 
    # Function: Process_R_Format
    # Parameters: the line, index(may not be necessary if we trim the string in
    #             parent function), and current (aka the instruction name)
    # Description: This function parses the current line of the input file, seperating
    #              the values into an object interpretation  
    ##################################################################################        
    def Process_R_Format(self, line, i, current):
        instr = current # log the current as the instruction
        current = ""
        i += 1 # get off space
        if (line[i] == "X"):
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()

        while(line[i] != ","):
            current += line[i]
            i += 1

        rd_num = current
        current = ""
        i += 1 # get off comma
        i += 1 # get off space

        if (line[i] == "X"):
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()


        while(line[i] != ","):
            current += line[i]
            i += 1

        rn_num = current
        current = ""
        i += 1 # get off comma
        i += 1 # get off space

        if (line[i] == "X"):
            i += 1
        else:
            print "Error: malformed instruction on line", self.current_line
            sys.exit()

        while(i < len(line)):
            current += line[i]
            i += 1

        rm_num = current
        opcode = self.instr_def['R-Format'][instr]
        self.Make_R_Format(instr, opcode, rm_num, rn_num, rd_num) # insert new object in instruction array with line serving as index
        return

    ##################################################################################
    # Function: Make_R_Format
    # Parameters: the parsed values provided by the parent function
    # Description: This function sorts the parameters and molds them into a more usable
    #              object format. This format makes actual instruction implementations
    #              more trivial.   
    ################################################################################## 
    def Make_R_Format(self, _name, _opcode, _rm, _rn, _rd):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'Rm': int(_rm), 'Rn': int(_rn), 'Rd': int(_rd)}})   
        return

    ##################################################################################
    # Function: execute
    # Parameters: none
    # Description: This is possibly the lynchpin function of this application. It is
    #              called to execute the current line of the application and move
    #              the program forward.
    ##################################################################################
    def execute(self):
        current_instr = self.program[self.current_line]
        instr_name = current_instr['name']

        print "Executing Line: " + self.str_current()
        
        # I-Format
        if (instr_name == 'ADDI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]

        elif (instr_name == 'SUBI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-",	immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            
        #D-Format
        elif (instr_name == 'LDUR'):
            Rt = self.program[self.current_line]['interpreted']['Rt']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            address = self.program[self.current_line]['interpreted']['address']
            mem_location = self.RFILE[Rn] + address
            self.RFILE[Rt] = self.MEM[mem_location]

        elif (instr_name == 'STUR'):
            Rt = self.program[self.current_line]['interpreted']['Rt']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            address = self.program[self.current_line]['interpreted']['address']
            mem_location = self.RFILE[Rn] + address
            self.MEM[mem_location] = self.RFILE[Rt]
            
        # R-Format
        elif (instr_name == 'ADD'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] + self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]

        elif (instr_name == 'SUB'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] - self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]


        self.current_line += 1
        if (self.current_line < len(self.program)):
            return self.str_current()# We kinda do nothing with this rn, mainly used to determine if we reached the end of the program
        else:
            return 'END'

    ##################################################################################
    # Function: str_current
    # Parameters: none
    # Description: Prints the full line that is currently be analyzed by the user. May
    #              need to be rewritten to return instead of print eventully.
    ##################################################################################
    def str_current(self):
        current_instr = self.program[self.current_line]
        output = ""
        
        name = current_instr['name']
        if (name in self.instr_def['I-Format']):
            Rd = current_instr['interpreted']['Rd']
            Rn = current_instr['interpreted']['Rn']
            imm = current_instr['interpreted']['imm']
            output = name + " X" + str(Rd) + ", X" + str(Rn) + ", #" + str(imm)

        elif (name in self.instr_def['D-Format']):
            Rt = current_instr['interpreted']['Rt']
            Rn = current_instr['interpreted']['Rn']
            addr = current_instr['interpreted']['address']
            output = name + " X" + str(Rt) + ", [X" + str(Rn) + ", #" + str(addr) + "]"


        elif (name in self.instr_def['R-Format']):
            Rd = current_instr['interpreted']['Rd']
            Rn = current_instr['interpreted']['Rn']
	    Rm = current_instr['interpreted']['Rm']
            output = name + " X" + str(Rd) + ", X" + str(Rn) + ", X" + str(Rm)

        return output


    ##################################################################################
    # Function: print_all
    # Parameters: none
    # Descriptions: This function prints all relevant information about the current
    #               line of the application.
    ##################################################################################
    def print_all(self):
        current_instr = self.program[self.current_line]
        name = current_instr['name']
        # The following line make it possible to interpret multiple formats
        if (name in self.instr_def['I-Format']):
            Rd = current_instr['interpreted']['Rd']
            Rn = current_instr['interpreted']['Rn']
            imm = current_instr['interpreted']['imm']
            print "Instruction: ", name, " X" + str(Rd), ", X" + str(Rn), ", #" + str(imm) 
            print "Instruction OpCode: ", current_instr['interpreted']['opcode'] 
            print "Write Register: X" + str(Rd), " ## Value in Write Register: ", self.RFILE[Rd]
            print "Register 1: X" + str(Rn), " ## Value in Register 1: ", self.RFILE[Rn]
            print "Immediate value: ", imm

        elif (name in self.instr_def['D-Format']):
            Rt = current_instr['interpreted']['Rt']
            Rn = current_instr['interpreted']['Rn']
            addr = current_instr['interpreted']['address']
            print "Instruction: ", name, " X" + str(Rt), ", [X" + str(Rn), ", #" + str(addr) + "]"
            print "Instruction OpCode: ", current_instr['interpreted']['opcode']
            print "Write Register: X" + str(Rt), " ## Value in Target Register: ", self.RFILE[Rt]
            print "Register 1: X" + str(Rn), " ## Value in Register 1: ", self.RFILE[Rn]
            print "Immediate value: ", addr
            
        elif (name in self.instr_def['R-Format']):
            Rd = current_instr['interpreted']['Rd']
            Rn = current_instr['interpreted']['Rn']
            Rm = current_instr['interpreted']['Rm']
            print "Instruction: ", name, " X" + str(Rd), ", X" + str(Rn), ", X" + str(Rm)
            print "Instruction OpCode: ", current_instr['interpreted']['opcode']
            print "Write Register: X" + str(Rd), " ## Value in Write Register: ", self.RFILE[Rd]
            print "Register 1: X" + str(Rn), " ## Value in Register 1: ", self.RFILE[Rn]
            print "Register 2: X" + str(Rm), " ## Value in Register 2: ", self.RFILE[Rm]


def digit_test(value):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if (value[0] != '+' and value[0] != '-' and (not value[0] in digits)):
        return False
    i = 1
    while (i < len(value)):
        if (not value[i] in digits):
            return False
        i += 1
    return True

def main():
    if (len(sys.argv) < 2):
        _input = raw_input("Please enter the name of the file containing the LEGv8 program: ")
        fileName = _input
    else:
        fileName = sys.argv[1]
        
    memory = []
    mem_idx = 0
    value = ""
    while (mem_idx < 1000 and value != 'done' and value != 'd'):
        value = raw_input("Please enter a value for memory index " + str(mem_idx) + " or 'done' when finished: ")
        if (digit_test(value)):
            memory.append(int(value))
            mem_idx += 1
        else:
            print "Error: non digit value entered, please enter numerical values only"
            
    controller = Control(fileName, memory)
    decision = raw_input("Enter 'step' for a step-by-step execution, or 'full' for a full-through execution: ")
    if (decision == 's' or decision == 'step'):
        controller.step()
    elif (decision == 'f' or decision == 'full'):
        controller.full()
    else:
        print "Input not recognized, defaulting to full-through"
        controller.full()

main()
