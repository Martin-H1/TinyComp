# TinyComp
A hobby cross compiler I'm building to learn more about how compilers work.

# Objective
Many years ago I worked for Kyan Software which built a Pascal compiler for 6502 machines. Like all multi-person projects, I
only worked on a piece of the project, and I didn't fully understand how the entire compiler worked. The purpose of this project
is to build a compiled language designed to produce code suitable for the limited architectures of the 6502 or 1802, and
understand the entire process end to end.

Also, architectures like the 1802 and 6502 are not good targets for C, as they lack a stack, or suitable stack relative addressing.
The compilers I’ve seen for them create a software stack, which results in a significant performance penalty. As a result
they are generally programmed in assembler, or in interpreters with a lower level of efficiency. The exception is the Forth
programming language which puts a lower burden on these machines, yet delivers a lot of features.

Since this won't be a self-host language, I will build a cross compiler in Python that implements the classic compilers phases
(e.g. tokenization, parsing, code generation). The output will be an assembler file suitable for compilation to a target machine.

# Methodology
My initial thinking was to remove stack variables from C, and see if what remains was useful. The results was a language where
all variables were static, and subroutine calls were allowed, but lack a local scope. The result was somewhat similar to BASIC
which was a popular eight bit language. But as the project progressed the peculiarities of C syntax created problems in forming
the abstract syntax tree (AST), which is a key step prior to code generation.

So I switched to Scheme syntax because the language syntax directly maps onto an AST. This made that process trivial so I
could focus on code generation.

# Tokenization
This process is implemented in the tokenizer.py module, and the code scans the input document, and transforms the text into an
array of tokens annotated by the token type and value. This includes the following types:
* unknown - a token that hasn't yet been recognized.
* comment - all the text between a semicolon and the end of line.
* identifier – symbol that identifies a value (e.g. label, variable).
* keyword – a word reserved for use by the language (e.g. abs, define, lambda, if).
* literal – a value that can be directly interpreted (e.g. an integer, character).
* operator – low level ALU operations (e.g. +, -, <, >)
* separator - syntax characters (e.g , ; ' parenthesis )
* string - a text literal delimited by quotes

# Parsing
This process is implemented in the schemeparser.py, and the token list is scanned and an abstract syntax tree is built.
The root of the tree is the global name space which contains S expressions which define either data, functions, or a
program entry point called main. Since S expressions are homoiconic, these amount to the same thing, execept functions
use the lambda keyword.

Because the s expression syntax is completely regular, translation into an AST is almost a 1 for 1 exercise.
The tree nodes consist of type field, a value, and array of child nodes.

# Code Generation
This process is controlled by the CodeGenerator class which scans the AST and emits assembler that correspond to the tree
elements. I assume the use of the Ophis assembler as it supports label scope, which is really handy in generating control
structures. In addition I asume that my own stack and print macros are used rather than directly generating the assembler
which is mush more verbose.

# Example
The factorial.scm is the sample I've used so far. Type this at the command line:
python tinylisp.py factorial.scm
Then look at the file factorial.asm which is the generated code.
