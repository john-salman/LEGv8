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

function start() {
    var filename;
    var rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout

    });

    rl.question("Please specify file name containing LEGv8 code: ", function(answer) {
        filename = answer;
        rl1.close();
    });

    let main = new Main(MEM, filename);

}

class Main {
    constructor(_MEM, _filename) {
        this.current_line = 0;
        this.MEM = JSON.parse(JSON.stringify(_MEM));
        this.flags = {
            Z,
            N,
            V,
            C,
        };
        this.RFILE[32] = [];
        this.main_obj = {current_line: this.current_line, MEM: this.MEM, flags: this.flags, RFILE: this.RFILE};

        this.instructions = new Instructions(this.main_obj);

        this.process_file(_filename);
    }

    process_file(_filename) {
    // need FileReader to open file
        var rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            terminal: false
        });

        let lineCount = 0;
        rl.on('line', function (line) {
            var current = "";
            var i = 0;
            while(line[i] !== " ") {
                current += line[i];
                i++;
            }

            if (this.instructions.I_type[current]) {
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
                let opcode = this.instructions.I_Type[instr].opcode;
                this.instructions.I_Type[instr].ARR[this.main_obj.current_line] = this.instructions.make_I_Type(opcode, imm, rn_num, rd_num);

            } else if (this.instructions.R_type[current]) {
                // process as R type
            } else if (this.instructions.D_type[current]) {
                // process as D type
            } else if (this.instructions.B_type[current]) {
                // process as B type
            } else if (this.instructions.CB_type[current]) {
                // process as CB type
            } else {
                // ITS A Label, we'll need to repeat the above
            }
        });

    }
}

class Instructions {
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
        this.R_Format = {
            opcode, Rm, shamt, Rn, Rd
        };
        this.I_Format = {
            opcode, immediate, Rn, Rd
        };
        this.D_Format = {
            opcode, data_trans_addr, buf, Rn, Rd
        };
        this.B_Format = {
            opcode, branch_addr
        };
        this.CB_Format = {
            opcode, cond_branch_addr, Rt
        };

        this.I_Type = {
            "ORRI": {execute: this.ORRI(this.line_num), opcode: 1424, ARR:[]},
            "EORI": {execute: this.EORI(this.line_num), opcode: 1680, ARR:[]},
            "ADDI": {execute: this.ADDI(this.line_num), opcode: 1160, ARR: []},
            "ADDIS": {execute: this.ADDIS(this.line_num), opcode: 1936 , ARR: []},
            "SUBI": {execute: this.SUBI(this.line_num), opcode: 1672, ARR: []},
            "SUBIS": {execute: this.SUBIS(this.line_num), opcode: 1928, ARR: []},
            "ANDI": {execute: this.ANDI(this.line_num), opcode: 1168, ARR: []},
            "ANDIS": {execute: this.ANDIS(this.line_num), /*opcode: ,*/ ARR: []},

        };
        this.B_Type = {
            "B": {execute: this.B(this.line_num), opcode: 160, ARR:[]},
            "BL": {execute: this.BL(this.line_num), opcode: 1184, ARR: []},

        };
        this.D_Type = {
            "STUR": {execute: this.STUR(this.line_num), opcode: 1984, ARR:[]},
            "LDUR": {execute: this.LDUR(this.line_num), opccode: 1986, ARR:[]},
            "STURH": {execute: this.STURH(this.line_num), opcode: 448, ARR:[]},
            "LDURH": {execute: this.LDURH(this.line_num), opccode: 450, ARR:[]},

        };
        this.R_Type = {
            "AND": {execute: this.AND(this.line_num), opcode: 1104, ARR: []},
            "ANDS": {execute: this.ANDS(this.line_num), opcode: 1104, ARR: []},
            "ADD": {execute: this.ADD(this.line_num), opcode: 1112, ARR: []},
            "ADDS": {execute: this.ADDS(this.line_num), opcode: 1368, ARR: []},
            "SUB": {execute: this.SUB(this.line_num), opcode: 1624, ARR: []},
            "SUBS": {execute: this.SUBS(this.line_num), opcode: 1880, ARR: []},
            "ORR": {execute: this.ORR(this.line_num), opcode: 1360, ARR: []},
            "EOR": {execute: this.EOR(this.line_num), opcode: 1616, ARR: []},
            "LSR": {execute: this.LSR(this.line_num), opcode: 1690, ARR: []},
            "LSL": {execute: this.LSL(this.line_num), opcode: 1691, ARR: []},
            "BR": {execute: this.BR(this.line_num), opcode: 1712, ARR: []}
        };
        this.CB_Type = {
          "CBZ": {execute: this.CBZ(this.line_num), opcode: 1440, ARR: []},
          "CBNZ": {execute: this.CBNZ(this.line_num), opcode: 1448, ARR: []},
        };

    }

    make_I_Type(opcode, imm, Rd, Rn) {
        return new this.I_Format(opcode, imm, Rd, Rn);
    }

    insert_instruction(line) {

    }

    ADD(idx) { // so we need to add flag setting logic
        let Rd = this.R_Type['ADD']['ARR'][idx]['Rd'];
        let Rn = this.R_Type['ADD']['ARR'][idx]['Rn'];
        let Rm = this.R_Type['ADD']['ARR'][idx]['Rm'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + this.main_obj.RFILE[Rm];
    }

    ADDI(idx) {
        let Rd = this.I_Type['ADD']['ARR'][idx]['Rd'];
        let Rn = this.I_Type['ADD']['ARR'][idx]['Rn'];
        let imm = this.I_Type['ADD']['ARR'][idx]['immediate'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + imm;
    }

    SUB(idx) {
        let Rd = this.R_Type['SUB']['ARR'][idx]['Rd'];
        let Rn = this.R_Type['SUB']['ARR'][idx]['Rn'];
        let Rm = this.R_Type['SUB']['ARR'][idx]['Rm'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] - this.main_obj.RFILE[Rm];
    }



}
