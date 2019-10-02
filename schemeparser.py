import sys
from tokenizer import Token, Tokenizer

class AbstractSyntaxTree:
    UNDEFINED = 0
    ROOT = 1

    COMMENT = 2
    DEFINE = 3
    DISPLAY = 4
    REFERENCE = 5

    BYTES = 6
    WORDS = 7

    IDENTIFIER = 8
    IF = 9
    LABEL = 10
    LAMBDA = 11
    LITERAL = 12
    SEXPR = 13
    STRING = 14

    EQUALS = 15
    ADD = 16
    SUB = 17
    MULTIPLY = 18
    DIVIDE = 19
    GREATER_THAN = 20
    LESS_THAN = 21

    STRING_POOL = 22

    DUP = 23

    NAMES = ["UNDEFINED", "ROOT", "COMMENT", "DEFINE", "DISPLAY", "REFERENCE", "BYTES", "WORDS", "IDENTIFIER", "IF", "LABEL", "LAMBDA", "LITERAL", "SEXPR", "STRING", "EQUALS", "ADD", "SUB", "MULTIPLY", "DIVIDE", "GREATER_THAN", "LESS_THAN", "STRING_POOL", "DUP"]

    def __init__(self, type = UNDEFINED, value = None, quoted=False):
        self.type = type
        self.value = value
        self.quoted = quoted
        self.children = [ ]

    def __str__(self):
        return "{}, value='{}', quoted={}, hash={}, children='{}'".format(AbstractSyntaxTree.NAMES[self.type], self.value, self.quoted, hash(self), len(self.children))

class SchemeParser:
    COMMENT = ";"
    KEYWORDS = ["abs", "and", "append", "apply", "bytes", "car", "cdr", "cond",
                "cons", "define", "display", "do", "dup", "filter", "if",
                "lambda", "length", "let", "map", "member", "modulo", "newline",
                "not", "or", "reverse", "words" ]
    OPERATORS = ["=", "+", "-", "*", "/", "<", ">"]
    SEPARATORS = "()'"

    def __init__(self):
        self.astRoot = AbstractSyntaxTree(AbstractSyntaxTree.ROOT)
        self.stringPool = AbstractSyntaxTree(type=AbstractSyntaxTree.STRING_POOL)
        self.astRoot.children.append(self.stringPool)

        self.tokenDispatch = {
            Token.COMMENT : self.parseComment,
            Token.IDENTIFIER : self.parseIdentifier,
            Token.KEYWORD : self.parseKeyword,
            Token.LITERAL : self.parseLiteral,
            Token.OPERATOR : self.parseKeyword,
            Token.SEPARATOR : self.parseSeparator,
            Token.STRING : self.parseString
        }

        self.keywordOperatorMap = {
            "abs" : None,
            "and" : None,
            "append" : None,
            "apply" : None,
            "bytes" : AbstractSyntaxTree.BYTES,
            "car" : None,
            "cdr" : None,
            "cond" : None,
            "cons" : None,
            "define" : AbstractSyntaxTree.DEFINE,
            "display" : AbstractSyntaxTree.DISPLAY,
            "do" : None,
            "dup" : AbstractSyntaxTree.DUP,
            "filter" : None,
            "if" : AbstractSyntaxTree.IF,
            "lambda" : AbstractSyntaxTree.LAMBDA,
            "length" : None,
            "let" : None,
            "map" : None,
            "member" : None,
            "modulo" : None,
            "newline" : None,
            "not" : None,
            "or" : None,
            "reverse" : None,
            "words" : AbstractSyntaxTree.WORDS,
            "*" : AbstractSyntaxTree.MULTIPLY,
            "+" : AbstractSyntaxTree.ADD,
            "-" : AbstractSyntaxTree.SUB,
            "/" : AbstractSyntaxTree.DIVIDE,
            "<" : AbstractSyntaxTree.LESS_THAN,
            "=" : AbstractSyntaxTree.EQUALS,
            ">" : AbstractSyntaxTree.GREATER_THAN
        }

    def parse(self, tokenList):
        self.parseSexpr(self.astRoot, tokenList, 0, False)

    def parseSexpr(self, astParent, tokenList, idx, quoted):
        while idx < len(tokenList) and tokenList[idx].value != ')':
            # don't pass the quote down to contained elements!
            idx = self.parseElement(astParent, tokenList, idx, False)
        return idx + 1

    def parseElement(self, astParent, tokenList, idx, quoted):
        dispatch = self.tokenDispatch.get(tokenList[idx].type)
        if dispatch != None:
            idx = dispatch(astParent, tokenList, idx, quoted)
        else:
            idx = idx + 1
        return idx

    def parseComment(self, astParent, tokenList, idx, quoted):
        comment = AbstractSyntaxTree(type=AbstractSyntaxTree.COMMENT,
                                     value = tokenList[idx].value,
                                     quoted=quoted)
        astParent.children.append(comment)
        return idx + 1

    def parseIdentifier(self, astParent, tokenList, idx, quoted):
        identifier = AbstractSyntaxTree(type = AbstractSyntaxTree.IDENTIFIER,
                                        value = tokenList[idx].value,
                                        quoted=quoted)
        astParent.children.append(identifier)
        return idx + 1

    def parseKeyword(self, astParent, tokenList, idx, quoted):
        type = self.keywordOperatorMap.get(tokenList[idx].value)
        if type != None:
            keyword = AbstractSyntaxTree(type = type)
            astParent.children.append(keyword)
        return idx + 1

    def parseLiteral(self, astParent, tokenList, idx, quoted):
        literal = AbstractSyntaxTree(type = AbstractSyntaxTree.LITERAL,
                                     quoted=quoted)
        literal.value = tokenList[idx].value
        astParent.children.append(literal)
        return idx + 1

    def parseSeparator(self, astParent, tokenList, idx, quoted):
        if tokenList[idx].value == '(':
            sexpr = AbstractSyntaxTree(type = AbstractSyntaxTree.SEXPR,
                                       quoted=quoted)
            astParent.children.append(sexpr)
            idx = self.parseSexpr(sexpr, tokenList, idx + 1, quoted)
        elif tokenList[idx].value == ')':
            idx = idx + 1
        elif tokenList[idx].value == "'":
            # parse the next element, but set the quoted state.
            idx = self.parseElement(astParent, tokenList, idx + 1, True)
        return idx

    def parseString(self, astParent, tokenList, idx, quoted):
        string = AbstractSyntaxTree(type = AbstractSyntaxTree.STRING)
        string.value = tokenList[idx].value
        self.stringPool.children.append(string)

        ref = AbstractSyntaxTree(type = AbstractSyntaxTree.REFERENCE)
        ref.value = str(hash(string))
        astParent.children.append(ref)

        return idx + 1

    def parseVector(self, astParent, tokenList, idx, quoted):
        while idx < len(tokenList) and tokenList[idx].value != ']':
            dispatch = self.tokenDispatch.get(tokenList[idx].type)
            if dispatch != None:
                idx = dispatch(astParent, tokenList, idx, quoted)
            else:
                idx = idx + 1
        return idx + 1
