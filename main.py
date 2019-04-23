import sys



class Control:
    def __init__(self, program, MEM):
        self.instructions = Instructions(program, MEM)
        
    def step(self):
        print("Please enter a command at the prompt below (enter 'h' or 'help' for help)" )
        command = false
        next = self.instructions.str_current()
        while(next != 'END' and command != 'exit' and command != 'e'):
            command = raw_input("[LEGv8]: ")
            if (command == 'n' or command == 'next'):
                next = self.instructions.execute()

            elif (command[0:5] == 'print' and len(command) > 5): # the print conditionals need to be modified to support p X0 or print X0 style commands
                self.instructions.print_specific(command)

            elif (command == 'p' or command == 'print'):
                self.instructions.print_all()

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
                
            else:
                print("Command not recognized, please enter 'help' for a full list of commands.")
        return

    def full(self):
        next = self.instructions.str_current()
        while (next != 'END'):
            next = self.instructions.execute()
        return

class Instructions: 

    def __init__(self, _program, _MEM):
        self.current_line = 0
        self.MEM = 0
        self.flags = {
            'Z': 0,
            'N': 0,
            'V': 0,
            'C': 0,
        }
        self.RFILE = [7, 5]

        self.program = []
 
        self.instr_def = {
        # I-Format                                                                                                                                                              
        #"ORRI": {  execute: self.ORRI(self.main_obj.current_line),  opcode: 1424 },                                                                                            
        #"EORI": {  execute: self.EORI(self.main_obj.current_line),  opcode: 1680 },                                                                                            
            'ADDI': 1160,
        #"ADDIS": { execute: self.ADDIS(self.main_obj.current_line), opcode: 1936 },                                                                                            
        #"SUBI": {  execute: self.SUBI(self.main_obj.current_line),  opcode: 1672 },                                                                                            
        #"SUBIS": { execute: self.SUBIS(self.main_obj.current_line), opcode: 1928 },                                                                                            
        #"ANDI": {  execute: self.ANDI(self.main_obj.current_line),  opcode: 1168 },                                                                                            
        #"ANDIS": { execute: self.ANDIS(self.main_obj.current_line), /*opcode: */ },                                                                                            
        # B-Format                                                                                                                                                              
        #"B": {     execute: self.B(self.main_obj.current_line),     opcode: 160 },                                                                                             
        #"BL": {    execute: self.BL(self.main_obj.current_line),    opcode: 1184 },                                                                                            
        # D-Format                                                                                                                                                              
        #"STUR": {  execute: self.STUR(self.main_obj.current_line),  opcode: 1984 },                                                                                            
        #"LDUR": {  execute: self.LDUR(self.main_obj.current_line),  opcode: 1986 },                                                                                            
        #"STURH": { execute: self.STURH(self.main_obj.current_line), opcode: 448 },                                                                                             
        #"LDURH": { execute: self.LDURH(self.main_obj.current_line), opcode: 450 },                                                                                             
        # R-Format                                                                                                                                                              
        #"AND": {   execute: self.AND(self.main_obj.current_line),   opcode: 1104 },                                                                                            
        #"ANDS": {  execute: self.ANDS(self.main_obj.current_line),  opcode: 1104 },                                                                                            
        #"ADD":  {  execute: self.ADD(self.main_obj.current_line),   opcode: 1112 },                                                                                            
        #"ADDS": {  execute: self.ADDS(self.main_obj.current_line),  opcode: 1368 },                                                                                            
        #"SUB": {   execute: self.SUB(self.main_obj.current_line),   opcode: 1624 },                                                                                            
        #"SUBS": {  execute: self.SUBS(self.main_obj.current_line),  opcode: 1880 },                                                                                            
        #"ORR": {   execute: self.ORR(self.main_obj.current_line),   opcode: 1360 },                                                                                            
        #"EOR": {   execute: self.EOR(self.main_obj.current_line),   opcode: 1616 },                                                                                            
        #"LSR": {   execute: self.LSR(self.main_obj.current_line),   opcode: 1690 },                                                                                            
        #"LSL": {   execute: self.LSL(self.main_obj.current_line),   opcode: 1691 },                                                                                            
        #"BR": {    execute: self.BR(self.main_obj.current_line),    opcode: 1712 },                                                                                            
        # CB-Format                                                                                                                                                             
        #"CBZ": {   execute: self.CBZ(self.main_obj.current_line),   opcode: 1440 },                                                                                            
            #"CBNZ": {  execute: self.CBNZ(self.main_obj.current_line),  opcode: 1448 },                                                                                        
        }
        self.process_file()

    def process_file(self):
        lineCount = 0
        line = "ADDI X1, X0, #12"
        current = ""
        i = 0
        while(line[i] != " "):
            current += line[i]
            i += 1


        if(self.instr_def[current]):
            instr = current # log the current as the instruction                                                                                                                     
            current = ""
            i += 1 # get off space                                                                                                                                                   

            if (line[i] == "X"):
                i += 1
            else:
                print("Error: malformed instruction")
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
                print("Error: malformed instruction")
                sys.exit()


            while(line[i] != ","):
                current += line[i]
                i += 1

            rn_num = current
            current = ""
            i += 1 # get off comma                                                                                                                                                   
            i += 1 # get off space                                                                                                                                                   

            if (line[i] == "#"):
                    i += 1
            else:
                print("Error: malformed instruction")
                sys.exit()

            while(i < len(line)):
                current += line[i]
                i += 1

            imm = current
            opcode = self.instr_def[instr]
            self.Make_I_Format(instr, opcode, imm, rn_num, rd_num) # insert new object in instruction array with line serving as index                                               
            print("Making a new thing with this", instr)
            return

    def Make_I_Format(self, _name, _opcode, _imm, _rn, _rd):
        self.program.append({'name': _name, 'interpreted': {'opcode': int(_opcode), 'imm': int(_imm), 'Rn': int(_rn), 'Rd': int(_rd)}})

    def execute(self):
        current_instr = self.program[self.current_line]
        instr_name = current_instr['name']
        
        print(self.program)
        if (instr_name == 'ADDI'):
            Rd = self.program[self.current_line]['interpreted']['Rd']
            Rn = self.program[self.current_line]['interpreted']['Rn']
            immediate = self.program[self.current_line]['interpreted']['imm']

            self.RFILE[Rd] = self.RFILE[Rn] + immediate
            print(self.RFILE[Rd])
            return

    def current(self):
        

def main():
    test = Control('test', 'test')
    test.instructions.execute()

main()
