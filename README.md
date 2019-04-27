We are developing this program to interpet user LEGv8 programs with an instruction subset. This program is intended 
as an educational tool so let us know if you want to add an instrcution. We are implementing the registers as 64 bit,
and are working to make the behavior as similar to assembly language as possible. The end goal is to connect this as
the backend of a public website, but for now we're building this as a command line utility.

If you have questions, encountered errors, or want to contribute (you will have to wait until we submit this for a class),
let us know at: jhnsalman@gmail.com. 

To Run: python main.py

This program will support the following commands:                                               
                                                                                              
    p(rint)     - Can be used with or without arguements to print the values of an instruction
                  Without arguements, the command will print all relevant information of an   
                  instruction. With arugements, the command will print the information of a   
                  register, instrution name, memory value, or constant.                       
                                                                                              
                  Example:                                                                    
                        p X11  =>  Register Value: 11                                         
                                   Register Contents: 43                                      
                                                                                              
    n(ext)      - Is used to move to the next instruction and execute the current. Command is 
                  verbose so it will talk through the steps of execution.                     
                                                                                              
                  Example:                                                                    
                        n  => Executing Line: ADDI X3, X4, #14                                
                              Value of Write Register before execution: 4                     
                              Evaluating interpreted expression: 8 + 14                       
                              Value of Write Register after execution: 20                     
                                                                                              
                              New Line: CBZ X3, LABEL                                         
                                                                                              
    exit        - Is used to exit the current instance of this program.                       
                                                                                              
    decimal     - Is used to set print outputs to decimal.                                    
                                                                                              
    hex         - Is used to set print outputs to hexadecimal.                                
                                                                                              
    binary      - Is used to set print outputs to binary.           
