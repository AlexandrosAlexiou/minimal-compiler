# Minimal++ Compiler

**Minimal++** is a minimal programming language developed for the Compilers course [@cs.uoi.gr](http://www.cs.uoi.gr/en/index.php?menu=m1) targeting the MIPS32 architecture.
* Intermediate code equivalent in C is ready to compile using any C compiler.
* Final code ready to assemble using MARS 4.5 [(MIPS Assembler and Runtime Simulator)](http://courses.missouristate.edu/KenVollmar/mars/)
<br/>

# File extensions
## `.min` Files
These are the actual Minimal++ programs.

## `.int` Files
These are the equivalent intermediate code files for every test program.

## `.c` Files 
These are the equivalent ANSI C files for every test program that does not have a function or procedure declaration.

## `.asm` Files 
These are the final code files for every test program in assembly [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture).
<br/>
<br/>

## Python version
`v3.7.4`

## Execution
Run: `./mppc.py [infile]`