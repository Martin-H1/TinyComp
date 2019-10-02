import unittest
from schemeparser import SchemeParser, AbstractSyntaxTree
from tokenizer import Token

class TestSchemeParser(unittest.TestCase):
    def test_c_tokenize(self):
        tokenList = (
            Token(type=Token.COMMENT, value='a comment.'),
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

        parser = SchemeParser()
        parser.parse(tokenList)
        self.processChildren(parser.astRoot, 0)

    def processChildren(self, node, level):
        print("    " * level + str(node))
        children = node.children
        ast = children[:1]
        while ast != []:
            self.processChildren(ast[0], level + 1)
            children = children[1:]
            ast = children[:1]

if __name__ == '__main__':
    unittest.main()
