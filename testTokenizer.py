import unittest
from tokenizer import Token, Tokenizer

class TestTokenizer(unittest.TestCase):

    def test_c_tokenize(self):
        COMMENT = "//"
        KEYWORDS = ["auto", "break", "case", "char", "const", "continue",
                    "default", "do", "double", "else", "enum", "extern",
                    "float", "for", "gosub", "goto", "if", "int", "long",
                    "register", "return", "short", "signed", "sizeof",
                    "static", "struct", "switch", "typedef", "union",
                    "unsigned", "void", "volatile", "while", "word"]
        OPERATORS = ["!", "=", "==", "!=", ">=", "+", "++", "-", "--", "*", "/",
                     "<", "<<", ">", ">>", "&", "&&", "|", "||"]
        SEPARATORS = ":;{}(),"

        tokenizer = Tokenizer(COMMENT, KEYWORDS, OPERATORS, SEPARATORS)

        source = " ".join( (
                "//a comment line\n",
                "const char * hello_world = \"Hello World!\"",
                "main: {\n",
                    "x = 5\n",
                    "while (x >= 0) {\n",
                        "x--\n",
                    "}\n",
                "}" ))
        tokenizer.tokenizeLine(source)
        tokenList = tokenizer.tokenList
        self.assertEqual( len(tokenList), 24)

        master = (
            Token(type=Token.COMMENT, value='a comment line'),
            Token(type=Token.KEYWORD, value='const'),
            Token(type=Token.KEYWORD, value='char'),
            Token(type=Token.OPERATOR, value='*'),
            Token(type=Token.IDENTIFIER, value='hello_world'),
            Token(type=Token.OPERATOR, value='='),
            Token(type=Token.STRING, value='Hello World!'),
            Token(type=Token.IDENTIFIER, value='main'),
            Token(type=Token.SEPARATOR, value=':'),
            Token(type=Token.SEPARATOR, value='{'),
            Token(type=Token.IDENTIFIER, value='x'),
            Token(type=Token.OPERATOR, value='='),
            Token(type=Token.LITERAL, value='5'),
            Token(type=Token.KEYWORD, value='while'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.IDENTIFIER, value='x'),
            Token(type=Token.OPERATOR, value='>='),
            Token(type=Token.LITERAL, value='0'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value='{'),
            Token(type=Token.IDENTIFIER, value='x'),
            Token(type=Token.OPERATOR, value='--'),
            Token(type=Token.SEPARATOR, value='}'),
            Token(type=Token.SEPARATOR, value='}') )

        idx = 0
        while idx < len(tokenList):
            self.assertEqual( tokenList[idx], master[idx])
            idx = idx + 1



    def test_scheme_tokenize(self):
        COMMENT = ";"
        KEYWORDS = ["abs", "and", "append", "apply", "car", "cdr", "cond",
                    "cons", "define", "display", "do", "filter", "if",
                    "lambda", "length", "let", "map", "member", "modulo",
                    "newline", "not", "or", "reverse" ]
        OPERATORS = ["=", "+", "-", "*", "/", "<", ">"]
        SEPARATORS = "()'"

        tokenizer = Tokenizer(COMMENT, KEYWORDS, OPERATORS, SEPARATORS)

        source = " ".join( (
                "; a comment.\n",
                "(define data '(1 2 3 4))\n",
                "(define factorial\n",
                "  (lambda (n)\n",
                "  (if (= n 0) 1\n",
                "      (* n (factorial (- n 1))))))",
                "(define hello_world",
                "  (lambda (display \"Hello World!\")))",
                "(define main (factorial 5))" ))

        tokenizer.tokenizeLine(source)
        tokenList = tokenizer.tokenList
        self.assertEqual( len(tokenList), 62)

        master = (
            Token(type=Token.COMMENT, value=' a comment.'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='define'),
            Token(type=Token.IDENTIFIER, value='data'),
            Token(type=Token.SEPARATOR, value="'"),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.LITERAL, value='1'),
            Token(type=Token.LITERAL, value='2'),
            Token(type=Token.LITERAL, value='3'),
            Token(type=Token.LITERAL, value='4'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='define'),
            Token(type=Token.IDENTIFIER, value='factorial'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='lambda'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.IDENTIFIER, value='n'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='if'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.OPERATOR, value='='),
            Token(type=Token.IDENTIFIER, value='n'),
            Token(type=Token.LITERAL, value='0'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.LITERAL, value='1'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.OPERATOR, value='*'),
            Token(type=Token.IDENTIFIER, value='n'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.IDENTIFIER, value='factorial'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.OPERATOR, value='-'),
            Token(type=Token.IDENTIFIER, value='n'),
            Token(type=Token.LITERAL, value='1'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='define'),
            Token(type=Token.IDENTIFIER, value='hello_world'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='lambda'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='display'),
            Token(type=Token.STRING, value='Hello World!'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.KEYWORD, value='define'),
            Token(type=Token.IDENTIFIER, value='main'),
            Token(type=Token.SEPARATOR, value='('),
            Token(type=Token.IDENTIFIER, value='factorial'),
            Token(type=Token.LITERAL, value='5'),
            Token(type=Token.SEPARATOR, value=')'),
            Token(type=Token.SEPARATOR, value=')') )

        idx = 0
        while idx < len(tokenList):
            self.assertEqual( tokenList[idx], master[idx])
            idx = idx + 1

if __name__ == '__main__':
    unittest.main()
