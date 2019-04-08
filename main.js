var readline = require('readline');

let foo = (x) => {
    return x + 4;
};

let current = 4;

let obj = {execute: foo(current)};

let answer = obj['execute'];

console.log("This be the answer: ", answer);

// Get process.stdin as the standard input object.

var standard_input = process.stdin;

// Set input character encoding.
standard_input.setEncoding('utf-8');

// Prompt user to input data in console.
console.log("Please input text in command line.");
/*
// When user input data and click enter key.
standard_input.on('data', function (data) {

    // User input exit.
    if(data === 'exit\n'){
        // Program exit.
        console.log("User input complete, program exit.");
        process.exit();
    }else
    {
        // Print user input in console.
        console.log('User Input Data : ' + data);
    }
});
*/
function start() {
   /*
    var filename;
    var rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout

    });

    rl.question("Please specify file name containing LEGv8 code: ", function(answer) {
        filename = answer;
        rl1.close();
    });
*/
   let MEM = [];
   let filename= "butt";
   let main = new Main(MEM, filename);

}

class Main {
    constructor(_MEM, _filename) {
        this.current_line = 0;
        this.MEM = JSON.parse(JSON.stringify(_MEM));
        this.flags = {
            Z: 0,
            N: 0,
            V: 0,
            C: 0,
        };
        this.RFILE = [7, 5];
        this.main_obj = {current_line: this.current_line, MEM: this.MEM, flags: this.flags, RFILE: this.RFILE};

        this.instructions = new Instructions(this.main_obj);

        this.process_file(_filename).then(() => this.instructions.execute());



    }

    process_file(_filename) {
    // need FileReader to open file
/*
        var rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            terminal: false
        });
*/


        let lineCount = 0;
       // rl.on('line', function (line) {
         var line = "ADDI X1, X0, #12";
            var current = "";
            var i = 0;
            while(line[i] !== " ") {
                current += line[i];
                i++;
            }

            if (this.instructions.instr_def[current]) {
                let instr = current; // log the current as the instruction
                current = "";
                i++;// get off space

                if (line[i] === "X") {
                    i++;
                } else {
                    console.log("Error: malformed instruction");
                    process.exit(1);
                }

                while(line[i] !== ",") {
                    current += line[i];
                    i++;
                }
                let rd_num = current;
                current = "";
                i++; // get off comma
                i++; // get off space

                if (line[i] === "X") {
                    i++;
                } else {
                    console.log("Error: malformed instruction");
                    process.exit(1);
                }

                while(line[i] !== ",") {
                    current += line[i];
                    i++;
                }
                let rn_num = current;
                current = "";
                i++; // get off comma
                i++; // get off space

                if(line[i] === "#") {
                    i++;
                } else {
                    console.log("Error: malformed instruction");
                    process.exit(1);
                }
                while(i < line.length) {
                    current += line[i];
                    i++;
                }
                let imm = current;
                let opcode = this.instructions.instr_def[instr].opcode;
                this.instructions.Make_I_Format(instr, opcode, imm, rn_num, rd_num); // insert new object in instruction array with line serving as index
                console.log("We're here chief");
            } else if (this.instructions.instr_def[current]) {
                // process as R type
            } else if (this.instructions.instr_def[current]) {
                // process as D type
            } else if (this.instructions.instr_def[current]) {
                // process as B type
            } else if (this.instructions.instr_def[current]) {
                // process as CB type
            } else {
                // Its a label, we'll need to mark it and repeat the above
            }

      //  });

    }
}

class Instructions {
    instr_def = {
        /*I-Format*/
        //"ORRI": {  execute: this.ORRI(this.main_obj.current_line),  opcode: 1424 },
        //"EORI": {  execute: this.EORI(this.main_obj.current_line),  opcode: 1680 },
        "ADDI": {  execute: this.ADDI(this.main_obj.current_line),  opcode: 1160 },
        //"ADDIS": { execute: this.ADDIS(this.main_obj.current_line), opcode: 1936 },
        //"SUBI": {  execute: this.SUBI(this.main_obj.current_line),  opcode: 1672 },
        //"SUBIS": { execute: this.SUBIS(this.main_obj.current_line), opcode: 1928 },
        //"ANDI": {  execute: this.ANDI(this.main_obj.current_line),  opcode: 1168 },
        //"ANDIS": { execute: this.ANDIS(this.main_obj.current_line), /*opcode: */ },
        /*B-Format*/
        //"B": {     execute: this.B(this.main_obj.current_line),     opcode: 160 },
        //"BL": {    execute: this.BL(this.main_obj.current_line),    opcode: 1184 },
        /*D-Format*/
        //"STUR": {  execute: this.STUR(this.main_obj.current_line),  opcode: 1984 },
        //"LDUR": {  execute: this.LDUR(this.main_obj.current_line),  opcode: 1986 },
        //"STURH": { execute: this.STURH(this.main_obj.current_line), opcode: 448 },
        //"LDURH": { execute: this.LDURH(this.main_obj.current_line), opcode: 450 },
        /*R-Format*/
        //"AND": {   execute: this.AND(this.main_obj.current_line),   opcode: 1104 },
        //"ANDS": {  execute: this.ANDS(this.main_obj.current_line),  opcode: 1104 },
        "ADD":  {  execute: this.ADD(this.main_obj.current_line),   opcode: 1112 },
        //"ADDS": {  execute: this.ADDS(this.main_obj.current_line),  opcode: 1368 },
        "SUB": {   execute: this.SUB(this.main_obj.current_line),   opcode: 1624 },
        //"SUBS": {  execute: this.SUBS(this.main_obj.current_line),  opcode: 1880 },
        //"ORR": {   execute: this.ORR(this.main_obj.current_line),   opcode: 1360 },
        //"EOR": {   execute: this.EOR(this.main_obj.current_line),   opcode: 1616 },
        //"LSR": {   execute: this.LSR(this.main_obj.current_line),   opcode: 1690 },
        //"LSL": {   execute: this.LSL(this.main_obj.current_line),   opcode: 1691 },
        //"BR": {    execute: this.BR(this.main_obj.current_line),    opcode: 1712 },
        /*CB-Format*/
        //"CBZ": {   execute: this.CBZ(this.main_obj.current_line),   opcode: 1440 },
        //"CBNZ": {  execute: this.CBNZ(this.main_obj.current_line),  opcode: 1448 },
    };


    constructor(_main_obj) {
        this.main_obj = _main_obj;

        /*
        may be better to do it like this:
        function Car(make, model, year) {
             this.make = make;
             this.model = model;
             this.year = year;
        }
        var myCar = new Car("Toyota", "Tacoma", "2002");
         */

        // This array will hold pointers to objects representing each line in the program
        this.program = [];

        //This object holds the definitions of each instruction


        function Line(name, interpreted) {
            return {name, interpreted }
        }

        /*OBJECT CONSTRUCTORS*/
        function Make_R_Format(_name, _opcode, _Rm, _shamt, _Rn, _Rd) {
            this.program[this.main_obj.current_line].push(new this.Line(_name, new this.R_Format(_opcode, _Rm, _shamt, _Rn, _Rd)));

        }

         this.Make_I_Format = (_name, _opcode, _imm, _Rd, _Rn) => {
            this.program[this.main_obj.current_line].push(new this.Line(_name, new this.I_Format(_opcode, _imm, _Rd, _Rn)));
        }

        function Make_D_Format(_name, _opcode, _data_trans_addr, _Rn, _Rt) {
            this.program[this.main_obj.current_line].push({name: _name, interpreted: new this.D_Format(_opcode, _data_trans_addr, _Rn, _Rt)});
            let new_line = this.main_obj.current_line + 1;
            this.main_obj.current_line = new_line;
        }

        function Make_B_Format(_name, _opcode, _branch_addr) {
            this.program[this.main_obj.current_line].push({name: _name, interpreted: new this.B_Format(_opcode, _branch_addr)});
            let new_line = this.main_obj.current_line + 1;
            this.main_obj.current_line = new_line;
        }

        function Make_CB_Format(_name, _opcode, _cond_branch_addr, _Rt) {
            this.program[this.main_obj.current_line].push({name: _name, interpreted: new this.CB_Format(_opcode, _cond_branch_addr, _Rt)});
            let new_line = this.main_obj.current_line + 1;
            this.main_obj.current_line = new_line;
        }


        /*OBJECT DEFINITIONS*/
        function R_Format ( _opcode, _Rm, _shame, _Rn, _Rd ){
            this.opcode = _opcode;
            this.Rm = _Rm;
            this.shamt = _shamt;
            this.Rn = _Rn;
            this.Rd = _Rd;
            this.print = Print_R(this);
        }

        this.I_Format = (_opcode, _immediate, _Rn, _Rd ) => {
            this.opcode = _opcode;
            this.immediate = _immediate;
            this.Rn = _Rn;
            this.Rd =_Rd;
            this.print = this.Print_I(this);
        }

        function D_Format ( _opcode, _data_trans_addr, _Rn, _Rt ) {
            this.opcode = _opcode;
            this.data_trans_addr = _data_trans_addr;
            this.Rn =_Rn;
            this.Rt = _Rt;
            this.print = this.Print_D(this)
        }

        function B_Format ( _opcode, _branch_addr) {
            this.opcode = _opcode;
            this.branch_addr = _branch_addr;
            this.print = this.Print_B(this);
        }

        function CB_Format (_opcode, _cond_branch_addr, _Rt) {
            this.opcode = _opcode;
            this.cond_branch_addr = _cond_branch_addr;
            this.Rt = _Rt;
            this.print = this.Print_CB(this);
        }



        function ADD(idx) { // so we need to add flag setting logic
            let Rd = this.program[idx].interpreted.Rd;
            let Rn = this.program[idx].interpreted.Rn;
            let Rm = this.program[idx].interpreted.Rm;
            this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + this.main_obj.RFILE[Rm];
        }

        this.ADDI = (idx) => {
            console.log(JSON.parse(JSON.stringify(this.program)));
            let Rd = this.program[idx]['interpreted'].Rd;
            let Rn = this.program[idx].interpreted.Rn;
            let Rm = this.program[idx].interpreted.immediate;
            this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + imm;
            let answer = this.main_obj.RFILE[Rd];
            return answer;
        };

        function SUB(idx) {
            let Rd = this.R_Type['SUB']['ARR'][idx]['Rd'];
            let Rn = this.R_Type['SUB']['ARR'][idx]['Rn'];
            let Rm = this.R_Type['SUB']['ARR'][idx]['Rm'];
            this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] - this.main_obj.RFILE[Rm];
        }

        function execute() {
            let current_instr = this.program[this.main_obj.current_line];
            let answer = this.instr_def[current_instr.name].execute;
            console.log("This should equal 24, it is: ", answer);
        }

    }


}

start();