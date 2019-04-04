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

class Main {
    constructor(_MEM) {
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
        let instructions = new Instructions(this.main_obj);
    }
}

class Instructions {
    constructor(_main_obj) {
        this.main_obj = _main_obj;

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
            "ORRI": {execute: this.ORRI(this.current_line), opcode: 1424, ARR:[]},
            "EORI": {execute: this.EORI(this.current_line), opcode: 1680, ARR:[]},
            "ADDI": {execute: this.ADDI(this.current_line), opcode: 1160, ARR: []},
            "ADDIS": {execute: this.ADDIS(this.current_line), opcode: 1936 , ARR: []},
            "SUBI": {execute: this.SUBI(this.current_line), opcode: 1672, ARR: []},
            "SUBIS": {execute: this.SUBIS(this.current_line), opcode: 1928, ARR: []},
            "ANDI": {execute: this.ANDI(this.current_line), opcode: 1168, ARR: []},
            "ANDIS": {execute: this.ANDIS(this.current_line), /*opcode: ,*/ ARR: []},

        };
        this.B_Type = {
            "B": {execute: this.B(this.current_line), opcode: 160, ARR:[]},
            "BL": {execute: this.BL(this.current_line), opcode: 1184, ARR: []},

        };
        this.D_Type = {
            "STUR": {execute: this.STUR(this.current_line), opcode: 1984, ARR:[]},
            "LDUR": {execute: this.LDUR(this.current_line), opccode: 1986, ARR:[]},
            "STURH": {execute: this.STURH(this.current_line), opcode: 448, ARR:[]},
            "LDURH": {execute: this.LDURH(this.current_line), opccode: 450, ARR:[]},

        };
        this.R_Type = {
            "AND": {execute: this.AND(this.current_line), opcode: 1104, ARR: []},
            "ANDS": {execute: this.ANDS(this.current_line), opcode: 1104, ARR: []},
            "ADD": {execute: this.ADD(this.current_line), opcode: 1112, ARR: []},
            "ADDS": {execute: this.ADDS(this.current_line), opcode: 1368, ARR: []},
            "SUB": {execute: this.SUB(this.current_line), opcode: 1624, ARR: []},
            "SUBS": {execute: this.SUBS(this.current_line), opcode: 1880, ARR: []},
            "ORR": {execute: this.ORR(this.current_line), opcode: 1360, ARR: []},
            "EOR": {execute: this.EOR(this.current_line), opcode: 1616, ARR: []},
            "LSR": {execute: this.LSR(this.current_line), opcode: 1690, ARR: []},
            "LSL": {execute: this.LSL(this.current_line), opcode: 1691, ARR: []},
            "BR": {execute: this.BR(this.current_line), opcode: 1712, ARR: []}
        };
        this.CB_Type = {
          "CBZ": {execute: this.CBZ(this.current_line), opcode: 1440, ARR: []},
          "CBNZ": {execute: this.CBNZ(this.current_line), opcode: 1448, ARR: []},
        };

    }

    ADD(idx) { // so we need to add flag setting logic
        let Rd = this.R_Type['ADD']['ARR'][idx]['Rd'];
        let Rn = this.R_Type['ADD']['ARR'][idx]['Rn'];
        let Rm = this.R_Type['ADD']['ARR'][idx]['Rm'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + this.main_obj.RFILE[Rm];
    }

    ADDI(idx) {
        let Rd = this.R_Type['ADD']['ARR'][idx]['Rd'];
        let Rn = this.R_Type['ADD']['ARR'][idx]['Rn'];
        let imm = this.R_Type['ADD']['ARR'][idx]['immediate'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] + imm;
    }

    SUB(idx) {
        let Rd = this.R_Type['SUB']['ARR'][idx]['Rd'];
        let Rn = this.R_Type['SUB']['ARR'][idx]['Rn'];
        let Rm = this.R_Type['SUB']['ARR'][idx]['Rm'];
        this.main_obj.RFILE[Rd] = this.main_obj.RFILE[Rn] - this.main_obj.RFILE[Rm];
    }



}
