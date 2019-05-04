import sys

###########################################################################################################################################
# Program: main.py
# Authors: John Salman, Tim Gallagher
# Description: This program allows user's to simulate execution of a LEGv8 program. Both in a standard full-through execution, and in a
#              a step-by-step psuedo debugger form. This application is intnended as an instructional tool and is thusly verbose when
#              being used in debugger (step) mode.
###########################################################################################################################################




###################################TO DO############################################
#          - parse and input CB-Format
#          - take in user-specified memory as input file
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
            elif (command == 'm' or command == 'memory'):
                self.instructions.printMem()
            elif (command == 'r' or command =='register'):
                self.instructions.printReg()
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
                print("    r(egister)  - Print all of the register file                                              ")
                print("                                                                                              ")
                print("    m(emory)    - Print all of the assigned memory                                            ")
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
        self.instructions.printMem()
        self.instructions.printReg()
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

        self.branch_args = ['EQ', 'NE', 'LT', 'LE', 'GT', 'GE'] 
        self.RFILE = [7, 5, -2, 6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.program = []
        self.prog_idx = 0 # current line being loaded into program[]
        self.labels = []

        
        # Place the name-value pairs in their appropriate spots as you go
        # NOTE: some opcodes may be incorrect/missing depending on source material
        
        #I-Format
        #"ANDIS": ,                                                                     

        # B-Format                                                       
        #"BL": 1184,
        
        # D-Format
        #"STURH": 448,                                                                      
        #"LDURH": 450,      

        # R-Format
         #"BR": 1712,
        
        # This object has three primary purposes:
        # 1. Is used to determine the format type of an instruction
        # 2. Obtain opcode value of instruction
        # 3. Labels can be determined by their exclusion from this set
        self.instr_def = {
            'I-Format': {
                "ADDI": 1160,
                "ADDIS": 1936,
                "SUBI": 1672,
                "SUBIS": 1928,
                "ANDI": 1168,
                "ORRI": 1424,
                "EORI": 1680,
            },
            'B-Format': {
                "B": 160,
            },
            'D-Format':{
                "STUR": 1984,
                "LDUR": 1986,
                "ANDS": 1104,
                "ADDS": 1368,
                "SUBS": 1880,
            },
            'R-Format': {
                "ADD": 1112,
                "SUB": 1624,
                "AND": 1104,
                "ORR": 1360,
                "EOR": 1616,
                "LSR": 1690,
                "LSL": 1691,
            },
            'CB-Format': {
                "CBZ": 1440,
                "CBNZ": 1448,
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
        branch_arg = ""
        i = 0
        while(lineCount < len(lines)):
            line = lines[lineCount]
            while(i < len(line) and line[i] != " " and line[i] != ":" and line[i] != "."):
                current += line[i]
                i += 1
            if (current != "" and current != "\n"):
                if (line[i] == "."):
                    i += 1
                    branch_arg += line[i:i+2]
                    if (not (branch_arg in self.branch_args)):
                        print "Error: Invalid branch conditional =>", line
                        sys.exit(1)
                    i += 2
                if (current in self.instr_def['I-Format']):
                    self.Process_I_Format(line, i, current)
                elif (current in self.instr_def['B-Format']):
                    self.Process_B_Format(line, i, current, branch_arg)
                elif (current in self.instr_def['D-Format']):
                    self.Process_D_Format(line, i, current)
                elif (current in self.instr_def['R-Format']):
                    self.Process_R_Format(line, i, current)
                elif (current in self.instr_def['CB-Format']):
                    self.Process_CB_Format(line, i, current)
                else:
                    self.Make_Label(current)
                    i += 1
                    while (i < len(line) and line[i] == " "): # get the space between the label and instruction  
                        i += 1
                    if (i != len(line)):
                        current = ""
                        while (i < len(line) and line[i] != " "):
                            current += line[i]
                            i += 1
                        if (current in self.instr_def['I-Format']):
                            self.Process_I_Format(line, i, current)
                        elif (current in self.instr_def['B-Format']):
                            self.Process_B_Format(line, i, current, branch_arg)
                        elif (current in self.instr_def['D-Format']):
                            self.Process_D_Format(line, i, current)
                        elif (current in self.instr_def['R-Format']):
                            self.Process_R_Format(line, i, current)
                        elif (current in self.instr_def['CB-Format']):
                            self.Process_CB_Format(line, i, current)
                        else:
                            print "Error: no instruction found in non-empty label line =>", line

            lineCount += 1
            current = ""
            i = 0
        self.Resolve_Undef_Labels()
        return

    ##################################################################################
    # Function: Make_Label
    # Parameters: the name of the label, and the line it was encountered on
    # Description: This function creates an association between a label and the line
    #              it was encountered on. This is so the program can interpret other
    #              branching instructions.
    ##################################################################################
    def Make_Label(self, label):
        self.labels.append({'label': label, 'line': self.prog_idx}) 

    ##################################################################################
    # Function: Resolve_Undef_Labels
    # Parameters: none
    # Description: This function searches for unresolved label instructions that may
    #              have been processed before the label was defined.
    ##################################################################################     
    def Resolve_Undef_Labels(self):
            i = 0
            prog_len = len(self.program)
            while (i < prog_len):
                current = self.program[i]
                if (current['name'] in self.instr_def['B-Format']
                    and current['interpreted']['label_line'] == -1):

                    j = 0
                    while (j < len(self.labels)):
                        if (self.labels[j]['label'] == current['interpreted']['label']):
                            current['interpreted']['label_line'] = self.labels[j]['line']
                            break
                        j += 1

                i += 1
                
    
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
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
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
        self.prog_idx += 1
        return

    ##################################################################################
    # Function: Process_B_Format
    # Parameters: the line, index(may not be necessary if we trim the string in
    #             parent function), and current (aka the instruction name)
    # Description: This function parses the current line of the input file, seperating
    #              the values into an object interpretation
    ##################################################################################
    def Process_B_Format(self, line, i, current, branch_arg):
        instr = current # log the current as the instruction
        current = ""
        i += 1 # we are still on the instr 
        while (i < len(line) and line[i] == ' '):
            i += 1
            
        if (i == len(line)):
            print "Error: malformed instruction =>", line
            sys.exit()
        else:    
            while(i < len(line) and line[i].isalpha()): # these loops append the digits into a temp variable
                current += line[i]
                i += 1

            label = current
            label_line = self.Find_Label(label)
            opcode = self.instr_def['B-Format'][instr]
            self.Make_B_Format(instr, opcode, label, label_line, branch_arg) # insert new object in instruction array with line serving as index
        return

    ##################################################################################
    # Function: Make_B_Format
    # Parameters: the parsed values provided by the parent function
    # Description: This function sorts the parameters and molds them into a more usable
    #              object format. This format makes actual instruction implementations
    #              more trivial.
    ##################################################################################
    def Make_B_Format(self, _name, _opcode, _label, _label_line, _branch_arg):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'label': _label, 'label_line': _label_line, 'branch_arg': _branch_arg}})
        self.prog_idx += 1
        return

    ##################################################################################
    # Function: Find_Label
    # Parameters: the string representing the label arguement to a branch instr
    # Description: This function finds the line associated with a label. If a label is
    #              not found the function returns one to make this instruction to be
    #              defined at the end.
    ##################################################################################   
    def Find_Label(self, label):
        i = 0
        while (i < len(self.labels)):
            if (self.labels[i]['label'] == label):
                return self.labels[i]['line']
            i += 1
        return -1
    
    
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
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
            sys.exit()
            
        if (line[i] == "X"): # Rn
            i += 1
        else:
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
            sys.exit() # we should explore a more graceful bomb out
            
        while(i < len(line) and line[i] != ']' and line[i] != ' '):
            current += line[i]
            i += 1
            
        if (line[i] == "]"): # Rn                                                                                                                                             
	    i += 1
        else:
            print "Error: malformed instruction =>", line
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
        self.prog_idx += 1
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
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
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
            print "Error: malformed instruction =>", line
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
        self.prog_idx += 1
        return

    ##################################################################################   
    # Function: Process_CB_Format                         
    # Parameters: the line, index(may not be necessary if we trim the string in                         
    #             parent function), and current (aka the instruction name) 
    # Description: This function parses the current line of the input file, seperating                 
    #              the values into an object interpretation                 
    ##################################################################################                                 
    def Process_CB_Format(self, line, i, current):
        instr = current # log the current as the instruction                                    
        current = ""
        i += 1 # we are still on the instr                                                             
        while (i < len(line) and line[i] == ' '):
            i += 1

        if (line[i] == "X"):
            i += 1
        else:
            print "Error: malformed instruction =>", line
            sys.exit()

        while (line[i] != ","):
            current += line[i]
            i += 1

        rt_num = current
        current = ""

        while (line[i] == " "):
            i += 1
        
        if (i == len(line)):
            print "Error: malformed instruction =>", line
            sys.exit()
        else:
            while(i < len(line) and line[i].isalpha()): # these loops append the digits into a temp variable                          
                current += line[i]
                i += 1

            label = current
            label_line = self.Find_Label(label)
            opcode = self.instr_def['CB-Format'][instr]
            self.Make_CB_Format(instr, opcode, rt_num, label, label_line) # insert new object in instruction array with line serving as index              
        return

    ##################################################################################                        
    # Function: Make_CB_Format                                                                                
    # Parameters: the parsed values provided by the parent function                                      
    # Description: This function sorts the parameters and molds them into a more usable        
    #              object format. This format makes actual instruction implementations
    #              more trivial.                                                                                                  
    ##################################################################################
    def Make_CB_Format(self, _name, _opcode, _rt, _label, _label_line, _branch_arg):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'Rt': int(_rt), 'label': _label, 'label_line': _label_line}})
        self.prog_idx += 1
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

        print " " # seperator
        print "Executing Line: " + self.str_current()

        # NOTE: if the instruction is branching, make sure to increment the current_line variable
        
        # I-Format
        if (instr_name == 'ADDI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        if (instr_name == 'ADDIS'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.set_flags(self.RFILE[Rd])
            print "Flags set by intruction:", self.flags
            self.current_line += 1
            
        elif (instr_name == 'SUBI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-",	immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'SUBIS'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-",    immediate
            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.set_flags(self.RFILE[Rd])
            print "Flags set by intruction:", self.flags
            self.current_line += 1
            
        elif (instr_name == 'ANDI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "&",    immediate
            self.RFILE[Rd] = self.RFILE[Rn] & immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'ORRI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "|",    immediate
            self.RFILE[Rd] = self.RFILE[Rn] | immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'EORI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "^",    immediate
            self.RFILE[Rd] = self.RFILE[Rn] ^ immediate
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        
        #B-Format
        elif (instr_name == 'B'):
            label = self.program[self.current_line]['interpreted']['label']
            label_line = self.program[self.current_line]['interpreted']['label_line']
            arg = self.program[self.current_line]['interpreted']['branch_arg']
            if (arg != ""):
                print "Branching with condition:", arg
                if (self.test_conditions()):
                    print "Jumping to label:", label
                    self.current_line = label_line
                else:
                    print "Branch Condition not met"
                    self.current_line += 1
            else:
                print "Jumping to label:", label
                self.current_line = label_line
            print "Now on line:", self.current_line
            if (self.current_line < len(self.program)):
                print "The instruction is now:", self.str_current()
            self.unset_flags()
            
        #D-Format
        elif (instr_name == 'LDUR'):
            Rt = self.program[self.current_line]['interpreted']['Rt']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            address = self.program[self.current_line]['interpreted']['address']
            mem_location = self.RFILE[Rn] + address
            print "Value:", self.MEM[mem_location], "loaded into register: X" + str(Rt)
            self.RFILE[Rt] = self.MEM[mem_location]
            self.current_line += 1
            
        elif (instr_name == 'STUR'):
            Rt = self.program[self.current_line]['interpreted']['Rt']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            address = self.program[self.current_line]['interpreted']['address']
            mem_location = self.RFILE[Rn] + address
            print "Value:", self.RFILE[Rt], "loaded into memory at location:", mem_location
            self.MEM[mem_location] = self.RFILE[Rt]
            self.current_line += 1
            
        # R-Format
        elif (instr_name == 'ADD'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] + self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'ADDS'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "+", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] + self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.set_flags(self.RFILE[Rd])
            print "Flags set by intruction:", self.flags
            self.current_line += 1
            
        elif (instr_name == 'SUB'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] - self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'SUBS'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "-", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] - self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.set_flags(self.RFILE[Rd])
            print "Flags set by intruction:", self.flags
            self.current_line += 1
            
        elif (instr_name == 'AND'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "&", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] & self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'ANDS'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "&", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] & self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.set_flags(self.RFILE[Rd])
            print "Flags set by intruction:", self.flags
            self.current_line += 1
            
        elif (instr_name == 'ORR'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "|", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] | self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'EOR'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "^", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] ^ self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'LSR'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], ">>", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] >> self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        elif (instr_name == 'LSL'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            Rm = self.program[self.current_line]['interpreted']['Rm']
            print "Value of Write Register before execution:", self.RFILE[Rd]
            print "Evaluating interpreted expression:", self.RFILE[Rn], "<<", self.RFILE[Rm]
            self.RFILE[Rd] = self.RFILE[Rn] << self.RFILE[Rm]
            print "Value of Write Register after execution:", self.RFILE[Rd]
            self.current_line += 1

        # CB-Format
        elif (instr_name == 'CBZ'):
            label = self.program[self.current_line]['interpreted']['label']
            label_line = self.program[self.current_line]['interpreted']['label_line']
            Rt = self.program[self.current_line]['interpreted']['Rt']
            if (self.RFILE[Rt] == 0):
                print "Zero condition met"
                self.current_line = label_line
            else:
                print "Zero condition not met"
                self.current_line += 1
            print "Now on line:", self.current_line
            if (self.current_line < len(self.program)):
                print "The instruction is now:", self.str_current()

        elif (instr_name == 'CBNZ'):
            label = self.program[self.current_line]['interpreted']['label']
            label_line = self.program[self.current_line]['interpreted']['label_line']
            Rt = self.program[self.current_line]['interpreted']['Rt']
            if (self.RFILE[Rt] != 0):
		print "Non-Zero condition met"
                self.current_line = label_line
            else:
                print "Non-Zero condition not met"
                self.current_line += 1
            print "Now on line:", self.current_line
            if (self.current_line < len(self.program)):
                print "The instruction is now:", self.str_current()
            
        if (self.current_line < len(self.program)):
            return self.str_current()# We kinda do nothing with this rn, mainly used to determine if we reached the end of the program
        else:
            return 'END'

    ##################################################################################
    # Function: test_conditions
    # Parameters: none
    # Description: This function is used to test if flags have been set by previous
    #              instructions. These flags will be unset after the call to this
    #              function by B and CBZ instruction.
    ################################################################################## 
    def test_conditions(self):
        branch_arg = self.program[self.current_line]['interpreted']['branch_arg']
        if (branch_arg == 'EQ'):
            return self.flags['Z'] == 1
        elif (branch_arg == 'ZE'):
            return self.flags['Z'] == 0
        elif (branch_arg == 'LT'):
            return self.flags['N'] != self.flags['V']
        elif (branch_arg == 'LE'):
            return not (self.flags['Z'] == 0 and self.flags['N'] == self.flags['V'])
        elif (branch_arg == 'GT'):
            return self.flags['Z'] == 0 and self.flags['N'] == self.flags['V']
        elif (branch_arg == 'GE'):
            return self.flags['N'] == self.flags['V']
        return False
        
    ##################################################################################
    # Function: unset_flags
    # Parameters: none
    # Description: Is used to reset flag values after it is used in a conditional 
    #              branching instruction.
    ##################################################################################
    def unset_flags(self):
        self.flags['N'] = 0
        self.flags['Z']	= 0
        self.flags['V']	= 0
        self.flags['C']	= 0

        
    ##################################################################################
    # Function: set_flags
    # Parameters: result, an integer holding the result of an execution
    # Description: Tests to see if the result of an execution meets the conditions
    #              necessary to set flag values.
    ##################################################################################
    def set_flags(self, result):
        if (result < 0):
            self.flags['N'] = 1
        elif (result == 0):
            self.flags['Z'] = 1
        # Including this outside the chain, as the negative and overflow flag can be set at the same time
        if (result < -9223372036854775807 or result > 9223372036854775807):
            self.flags['V'] = 1
            
        
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

        elif (name in self.instr_def['B-Format']):
            label = current_instr['interpreted']['label']
            arg = current_instr['interpreted']['branch_arg']
            if (arg != ""):
                arg = "." + arg
            output = name + arg + ' ' + label
            
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

        elif (name in self.instr_def['CB-Format']):
            label = current_instr['interpreted']['label']
            Rt = current_instr['interpreted']['Rt']
            output = name + " X" + str(Rt) + ", " + label
            
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
        if (name in self.instr_def['I-Format']):
            Rd = current_instr['interpreted']['Rd']
            Rn = current_instr['interpreted']['Rn']
            imm = current_instr['interpreted']['imm']
            print "Instruction: ", name, " X" + str(Rd), ", X" + str(Rn), ", #" + str(imm) 
            print "Instruction OpCode: ", current_instr['interpreted']['opcode'] 
            print "Write Register: X" + str(Rd), " ## Value in Write Register: ", self.RFILE[Rd]
            print "Register 1: X" + str(Rn), " ## Value in Register 1: ", self.RFILE[Rn]
            print "Immediate value: ", imm

        elif (name in self.instr_def['B-Format']):
            label = current_instr['interpreted']['label']
            label_line = current_instr['interpreted']['label_line']
            arg = current_instr['interpreted']['branch_arg']
            if (arg != ""):
                print "Instruction: ", name + "." + arg, label
                print "Condition on branch:", arg
            else:
                print "Instruction:", name, label
            print "Instruction OpCode: ", current_instr['interpreted']['opcode']
            print "Address of label: ", label_line


        elif (name in self.instr_def['D-Format']):
            Rt = current_instr['interpreted']['Rt']
            Rn = current_instr['interpreted']['Rn']
            addr = current_instr['interpreted']['address']
            print "Instruction: ", name, " X" + str(Rt), ", [X" + str(Rn), ", #" + str(addr) + "]"
            print "Instruction OpCode: ", current_instr['interpreted']['opcode']
            print "Target Register: X" + str(Rt), " ## Value in Target Register: ", self.RFILE[Rt]
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

        elif (name in self.instr_def['CB-Format']):
            label = current_instr['interpreted']['label']
            label_line = current_instr['interpreted']['label_line']
            Rt = current_instr['interpreted']['Rt']
            print "Instruction: ", name, "X" + str(Rt), ",", label
            print "Instruction OpCode: ", current_instr['interpreted']['opcode']
            print "Target Register: X" + str(Rt), " ## Value in Target Register: ", self.RFILE[Rt]
            print "Address of label: ", label_line
     
            
    def printMem(self):
        k = len(self.MEM)
        print "Mem", " ", "Val"
        for i in range(k):
            print i, " ", " ", self.MEM[i]

    def printReg(self):
        k = len(self.RFILE)
        print "Reg", " ", "Val"
        for i in range(k):
            print "X"+str(i), " ", " ", self.RFILE[i]



def digit_test(value):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
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
        elif (value != 'd' and value != 'done'):
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
