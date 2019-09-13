import sys
from tokenizer import Token, Tokenizer

class AbstractSyntaxToken:
    UNDEFINED = 0
    ASSIGN = 1
    DATA = 2

    GOSUB = 3
    GOTO = 4
    HALT = 5
    IF = 6
    WHILE = 7

    INC = 8
    DEC = 9
    NEG = 10
    ADD = 11
    SUB = 12

    LABEL = 13
    LITERAL = 14

    DEREFERENCE = 15

    NAMES = ["UNDEFINED", "ASSIGN", "DATA", "GOSUB", "GOTO", "HALT", "IF", "WHILE", "INC", "DEC", "NEG", "ADD", "SUB", "LABEL", "LITERAL"]

    def __init__(self):
        self.type = AbstractSyntaxToken.UNDEFINED
        self.children = [ ]

class Parser:
    COMMENT = "//"
    KEYWORDS = ["auto", "break", "case", "char", "const", "continue",
                "default", "do", "double", "else", "enum", "extern",
                "float", "for", "gosub", "goto", "if", "int", "long",
                "register", "return", "short", "signed", "sizeof",
                "static", "struct", "switch", "typedef", "union",
                "unsigned", "void", "volatile", "while", "word"]
    OPERATORS = "=+-*/<>&|"
    SEPARATORS = ":;{}(),"

    def __init__(self):
        self.astRoot = []

    def parse(self, tokenList):
        for token in tokenList:
            print(token)

class CodeGenerator:
    def __init__(self):
        self.astRoot = []

tokenizer = Tokenizer(Parser.COMMENT,
                      Parser.KEYWORDS,
                      Parser.OPERATORS,
                      Parser.SEPARATORS)
tokenizer.tokenizeFile(sys.argv[1])
parser = Parser()
parser.parse(tokenizer.tokenList)
