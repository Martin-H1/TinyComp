from pathlib import Path
from schemeparser import SchemeParser, AbstractSyntaxTree
from tokenizer import Token, Tokenizer
import sys

class CodeGenerator:
    def __init__(self, astRoot):
        self.astDispatch = {
            AbstractSyntaxTree.DEFINE : self.processDefine,
            AbstractSyntaxTree.DISPLAY : self.processDisplay,
            AbstractSyntaxTree.DUP : self.processDup,
            AbstractSyntaxTree.EQUALS : self.processEquals,
            AbstractSyntaxTree.IDENTIFIER : self.processIdentifier,
            AbstractSyntaxTree.IF : self.processIf,
            AbstractSyntaxTree.LAMBDA : self.processLambda,
            AbstractSyntaxTree.LITERAL : self.processLiteral,
            AbstractSyntaxTree.MULTIPLY : self.processMultiply,
            AbstractSyntaxTree.ROOT : self.processNode,
            AbstractSyntaxTree.SEXPR : self.processSexpr,
            AbstractSyntaxTree.STRING : self.processNode,
            AbstractSyntaxTree.STRING_POOL : self.processStrings,
            AbstractSyntaxTree.SUB : self.processSub,
            AbstractSyntaxTree.BYTES : self.processBytes,
            AbstractSyntaxTree.WORDS : self.processWords
        }
        self.astRoot = astRoot

    def process(self, outputName):
        with open(outputName, "w") as self.of:
            # Recursively process the arguments.
            self.processCdr(self.astRoot, None, 0, 0)

    # process the first item of a list.
    def processCar(self, parent, node, level, idx):
        dispatch = self.astDispatch.get(node.type)
        if dispatch != None:
            idx = dispatch(parent, node, level, idx)
        else:
            idx = idx + 1
        return idx

    # process the rest of a list.
    def processCdr(self, parent, node, level, idx):
        while idx < len(parent.children):
            idx = self.processCar(parent, parent.children[idx], level, idx)
        return idx

    def processDefine(self, parent, node, level, idx):
        # The next token's value is what define is operating on.
        idx = idx + 1
        if parent.children[idx].type != AbstractSyntaxTree.IDENTIFIER:
            raise Exception('Define requires identifier')

        self.of.write(parent.children[idx].value + ":\n")
        return idx + 1

    def processDisplay(self, parent, node, level, idx):
        # The next token's value is what display is operating on.
        idx = idx + 1

        if parent.children[idx].type == AbstractSyntaxTree.LITERAL:
            self.of.write("\t`print {}\n".format(parent.children[idx].value))
        elif parent.children[idx].type == AbstractSyntaxTree.REFERENCE:
            self.of.write("\t`pushi ref_{}\n".format(parent.children[idx].value))
            self.of.write("\tjsr println\n")
        else:
            raise Exception('Display requires lieral or identifier')
        return idx + 1

    def processDup(self, parent, node, level, idx):
        print("dup")
        self.of.write("\t`dup\n")
        return idx + 1

    def processEquals(self, parent, node, level, idx):
        # Recursively process the arguments.
        idx = self.processCdr(parent, node, level, idx + 1)

        self.of.write("\tjsr equals16\n".format(node.value))
        return idx

    def processIdentifier(self, parent, node, level, idx):
        if idx == 0:
            # Recursively process the arguments.
            idx = self.processCdr(parent, node, level, idx + 1)
            self.of.write("\tjsr {}\n".format(node.value))
        else:
            self.of.write("\t`pushv {}\n".format(node.value))
            idx = idx + 1
        return idx

    def processIf(self, parent, node, level, idx):
        idx = idx + 1

        # Recursively process the test expression.
        idx = self.processCar(parent, parent.children[idx], level + 1, idx)
        self.of.write(".scope\n")

        # Generate a branch to the else on false.
        self.of.write("\tbne _else\n")

        idx = self.processCar(parent, parent.children[idx], level + 1, idx)
        # Generate the branch to endif
        self.of.write("\tbra _endif\n_else:\n")

        # Generate the else code
        idx = self.processCdr(parent, parent.children[idx], level + 1, idx)

        # Generate the label for the endif branch.
        self.of.write("_endif:\n")
        self.of.write(".scend\n\n")
        return idx

    def processLambda(self, parent, node, level, idx):
        idx = idx + 1

        # Check to see if body is missing.
        if len(parent.children) < 2:
            raise Exception('Lambda requires a body and optional arguments.')

        if len(parent.children) >=3:
            # ignore arguments for now.
            idx = idx + 1

        self.of.write(".scope\n")

        # Recursively process the body.
        idx = self.processCdr(parent, node, level, idx)

        # A function has a return operation.
        self.of.write("\trts\n")
        self.of.write(".scend\n\n")
        return idx

    def processLiteral(self, parent, node, level, idx):
        self.of.write("\t`pushi {}\n".format(parent.children[idx].value))
        return idx + 1

    def processMultiply(self, parent, node, level, idx):
        idx = idx + 1

        # Check to see if arguments are missing.
        if len(parent.children) < 3:
            raise Exception('Multiplication requires two arguments.')

        # process the arguments which leave result on data stack.
        idx = self.processCdr(parent, node, level, idx)

        # Now perform process the argumentsA function has a return operation.
        self.of.write("\tjsr mul16\n")
        return idx

    def processNode(self, parent, node, level, idx):
        print("    " * level + str(node))
        return idx + 1

    def processSexpr(self, parent, node, level, idx):
        # Quoted S expressions are not processed.
        if node.quoted == True:
            return idx + 1

        # Recursively process the rest of the children.
        self.processCdr(node, node.children, level + 1, 0)

        # Let the parent process our siblings.
        return idx + 1

    def processString(self, parent, node, level, idx):
        print("    " * level + str(node))
        return idx + 1

    def processStrings(self, parent, node, level, idx):
        for element in node.children:
            self.of.write("ref_{}:\t.byte \"{}\",0\n".
                          format(hash(element), element.value))
        return idx + 1

    def processSub(self, parent, node, level, idx):
        idx = idx + 1

        # Check to see if arguments are missing.
        if len(parent.children) < 3:
            raise Exception('Subtraction requires two arguments.')

        # process the arguments which leave result on data stack.
        idx = self.processCdr(parent, node, level, idx)

        # Now perform process the argumentsA function has a return operation.
        self.of.write("\tjsr sub16\n")
        return idx

    def processBytes(self, parent, node, level, idx):
        idx = idx + 1
        next = parent.children[idx]

        # The next token's value should be a quoted sexpr.
        if next.type != AbstractSyntaxTree.SEXPR and next.quoted == False:
           raise Exception('Bytes requires a quoted sxpr.')

        self.of.write("\t.byte ")
        self. processQuotedList(parent, next, level, 0)
        return idx + 1

    def processWords(self, parent, node, level, idx):
        idx = idx + 1
        next = parent.children[idx]

        # The next token's value should be a quoted sexpr.
        if next.type != AbstractSyntaxTree.SEXPR and next.quoted == False:
           raise Exception('Words requires a quoted sxpr.')

        self.of.write("\t.word ")
        self. processQuotedList(parent, next, level, 0)
        return idx + 1

    def processQuotedList(self, parent, node, level, idx):
        while idx < len(node.children):
            self.of.write(node.children[idx].value)
            idx = idx + 1
            if idx < len(node.children):
                self.of.write(", ")
        self.of.write("\n")
        return idx

tokenizer = Tokenizer(SchemeParser.COMMENT,
                      SchemeParser.KEYWORDS,
                      SchemeParser.OPERATORS,
                      SchemeParser.SEPARATORS)
tokenizer.tokenizeFile(sys.argv[1])
parser = SchemeParser()
parser.parse(tokenizer.tokenList)

try:
    generator = CodeGenerator(parser.astRoot)
    generator.process(Path(sys.argv[1]).stem + ".asm")
except Exception as ex:
    print(ex)
