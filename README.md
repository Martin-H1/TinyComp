# TinyComp
A hobby cross compiler I'm building to learn more about how compilers work.

# Objective
Architectures like the 1802 and 6502 are not good targets for C, as they lack a stack, or suitable stack relative addressing.
The compilers I’ve seen for them create a software stack, and that results in a significant performance penalty. As a result
they are generally programmed in assembler, or in interpreters with a lower level of efficiency. Ideally a compiled language
could be designed which produces suitable code for their limited architectures, at a higher level of semantic abstraction and
portability than assembler, but with similar performance. 

# Methodology
The obvious approach is to remove stack variables from C, and see if what remains is useful. The results is a language where
all variables are static, and subroutine calls are allowed, but lack a local scope. The result is somewhat similar to BASIC
which was a popular eight bit language, so the approach I plan to take is a BASIC/C mashup.

I won't self-host and instead build a cross compiler in Python that implements the classic compilers phases (e.g. tokenization,
parsing, code generation). The output will be an assembler file suitable for compilation to a target machine.

# Tokenization
This process scans the input document and transforms the text into an array of tokens annotated by the token type and value.
This includes the following types:
* identifier – symbol that identifies a value (e.g. label, variable).
* keyword – a word reserved for use by the language (e.g. char, for, goto, if, short).
* literal – a value that can be directly interpreted (e.g. an integer, character).
* operator – low level ALU operations (e.g. +, -, <, >)
* separator - syntax characters (e.g , ; )
* string - a text literal delimited by quotes

# Parsing
This process is where the rubber meets the road. The token list is scanned and an abstract syntax tree is built. The root of
the tree is the global name space which contains the static variables, and the program entry point called main.

# Code Generation
This process is controlled by a target command line option to produce code suitable for a specific target architecture. It 
walks the AST and emits corresponding assembler constructs. Final object file generation is done via an assembler for the
target platform.
