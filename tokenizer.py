"""
This module contains a simple tokenizer for use in the tiny compiler.
This tokenizer performs demarcation and minimal classification of
the a string of input characters from a file.
"""

class Token:
    UNKNOWN = 0
    COMMENT = 1
    IDENTIFIER = 2
    KEYWORD = 3
    LITERAL = 4
    OPERATOR = 5
    SEPARATOR = 6
    STRING = 7

    NAMES = ["UNKNOWN", "COMMENT", "IDENTIFIER", "KEYWORD", "LITERAL", "OPERATOR", "SEPARATOR", "STRING"]

    def __init__(self):
        self.type = Token.UNKNOWN
        self.value = ""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.type == other.type and self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "type='{}', value='{}'".format(Token.NAMES[self.type], self.value)

    def appendChar(self, first):
        self.value = self.value + first

class Tokenizer:
    def __init__(self, comment, keywords, operators, separators):
        """
        Initializer that sets up the tokenizer for processing. It also
        accepts varaious parameters that demarcate tokens.

        Arguments:
        comment -- the character(s) that indicate a comment line.
        keywords -- a list of languages keywords for classifications.
        operators -- the characters that are operators for classification.
        separators -- the characters that separate elements of syntax.
        """

        self.comment = comment
        self.keywords = keywords
        self.operators = operators
        self.separators = separators
        self.tokenList = []
        self.tokenDispatch = {
            Token.UNKNOWN : self.processUnknown,
            Token.COMMENT : self.processComment,
            Token.IDENTIFIER : self.processIdentifier,
            Token.LITERAL : self.processLiteral,
            Token.STRING : self.processString
        }

    def tokenizeFile(self, filename):
        """
        Opens a file by name and tokenizees it a line at a time.

        Arguments:
        filename -- the name of the file.
        """
        self.workToken = Token()
        with open(filename) as sourcefile:
            for line in sourcefile:
                self.tokenizeLine(line)

    def tokenizeLine(self, line):
        while line != "":
            dispatch = self.tokenDispatch.get(self.workToken.type)
            line = dispatch(line[:1], line[1:], line)

    """
    The following methods are dispatchers that all have the same
    argument signature. This allows calling them via a dispatch
    table based upon the type of token identified.
    """
    def processUnknown(self, first, rest, line):
        """
        Default state for the tokenizer. If it identifies the token type
        it will transition to that state which results in that dispatcher
        getting called.

        Arguments:
        first -- the first character in the line.
        rest -- the rest of the chacters in the line.
        line -- the entire line to parse.

        Returns:
        the characters that were not consumed by the processor.
        """
        if line.startswith(self.comment):
            self.workToken.type = Token.COMMENT
            rest = rest[1:]
        elif first.isalpha() or first == "_":
            self.workToken.type = Token.IDENTIFIER
            self.workToken.appendChar(first)
        elif first.isnumeric():
            self.workToken.type = Token.LITERAL
            self.workToken.appendChar(first)
        elif first in self.separators:
            self.appendToken(Token.SEPARATOR, first)
        elif first in self.operators:
            # check for double operators (e.g. ++, --, ==, etc)
            if rest.startswith(first):
                rest = rest[1:]
            self.appendToken(Token.OPERATOR, first + first)
        elif first == "\"":
            self.workToken.type = Token.STRING
        return rest

    def processComment(self, first, rest, line):
        if first == "\n":
            self.appendToken(Token.COMMENT, self.workToken.value)
        else:
            self.workToken.appendChar(first)
        return rest

    def processIdentifier(self, first, rest, line):
        if first.isalnum() or first == "_":
            self.workToken.appendChar(first)
            return rest
        elif not first.isalpha():
            if self.workToken.value in self.keywords:
                self.appendToken(Token.KEYWORD, self.workToken.value)
            else:
                self.appendToken(Token.IDENTIFIER, self.workToken.value)
            return line

    def processLiteral(self, first, rest, line):
        if first.isnumeric():
            self.workToken.appendChar(first)
            return rest
        else:
            self.appendToken(Token.LITERAL, self.workToken.value)
            return line

    def processString(self, first, rest, line):
        if first != "\"":
            self.workToken.appendChar(first)
        else:
            self.appendToken(Token.STRING, self.workToken.value)
        return rest

    def appendToken(self, type, value):
        """
        Adds a token to the end of the list and resets the working token.

        Arguments:
        type -- the type of the token to add.
        value -- the text contents of the token.
        """

        self.workToken.type = type
        self.workToken.value = value
        self.tokenList.append(self.workToken)

        # Reset tokenizer state.
        self.workToken = Token()
