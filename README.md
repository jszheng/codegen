# codegen
combined tools for code generation

## modules
* [pyverilog](https://github.com/PyHDI/Pyverilog)
* [veriloggen](https://github.com/PyHDI/veriloggen)
* ANTLR4 Verilog parser for python
* Meta HDL

## TODO

### Philosophy:
Simple, Extendable, Easy change, Write less code

### meta data describe
* type     : type system, including build-in type for C/C++/Verilog/SV, struct and union
* bundle   : a group of signal, with type but no direction
* protocol : specialized bundle contains control signals
* interface: protocol with payload bundle or just input/output
* component: interface, code, instance and its connections 

mixed simple dsl parser and python embedded code. 
