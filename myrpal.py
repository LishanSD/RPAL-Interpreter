import sys
import Scanner
from Scanner import Screener
import controlStructure
from cseMachine import CSEMachine
import os
from Node import ASTNode


#  Parser class that contains methods for parsing tokens and building an AST
class Parser:
    def __int__(self, Tokens):  # Initializes the parser with a list of tokens
        self.tokens = Tokens
        self.curr_token = None
        self.index = 0

    def read(self): # Reads the next token and processes it
        if self.curr_token.type in [Scanner.Type.ID, Scanner.Type.INT,
                                       Scanner.Type.STRING] :

            terminalNode = ASTNode( str(self.curr_token.type))
            terminalNode.value= self.curr_token.value
            stack.append(terminalNode)

        if self.curr_token.value in  ['true', 'false', 'nil', 'dummy']:

            terminalNode = ASTNode(str(self.curr_token.type))
            terminalNode.value = self.curr_token.value
            stack.append(terminalNode)

        self.index += 1

        if (self.index < len(self.tokens)):
            self.curr_token = self.tokens[self.index]



    def buildTree(self, token, ariness):  # Builds an AST subtree
        global stack

        node = ASTNode(token)

        node.value = None
        node.sourceLineNumber = -1
        node.child = None
        node.sibling = None
        node.previous = None

        while ariness > 0:

            child = stack[-1]
            stack.pop()
            if node.child is not None:
                child.sibling = node.child
                node.child.previous = child
            node.child = child

            node.sourceLineNumber = child.sourceLineNumber
            ariness -= 1


        stack.append(node) 
        for node in stack:
            pass
       
    # Parsing expressions
    def procE(self):
 
        match self.curr_token.value:

            case 'let':
                self.read()
                self.procD()

                if self.curr_token.value != 'in':
                    return

                self.read()
                self.procE()
                self.buildTree("let", 2)

            case 'fn':
                n = 0
                self.read()
                while self.curr_token.type == Scanner.Type.ID or self.curr_token.value == '(':
                    self.procVb()
                    n += 1

                if n == 0:
                    return

                if self.curr_token.value != '.':
                    return

                self.read()
                self.procE()
                self.buildTree("lambda", n+1)

            case _:
                self.procEw()

    def procEw(self):
        self.procT()
        if self.curr_token.value == 'where':
            self.read()
            self.procDr()
            self.buildTree("where", 2)

    def procT(self):
        self.procTa()

        n = 0
        while self.curr_token.value == ',':
            self.read()
            self.procTa()
            n += 1
        if n > 0:
            self.buildTree("tau", n + 1)
        else:
            pass

    def procTa(self):
        self.procTc()
        while self.curr_token.value == 'aug':
            self.read()
            self.procTc()
            self.buildTree("aug", 2)

    def procTc(self):
        self.procB()
        if self.curr_token.type == Scanner.Type.TERNARY_OPERATOR:
            self.read()
            self.procTc()

            if self.curr_token.value != '|':
                print("Error: | is expected")
                return
            self.read()
            self.procTc()
            self.buildTree("->", 3)

    def procB(self):

        self.procBt()
        while self.curr_token.value == 'or':
            self.read()
            self.procBt()
            self.buildTree("or", 2)

    def procBt(self):
        self.procBs()
        while self.curr_token.value == '&':
            self.read()
            self.procBs()
            self.buildTree("&", 2)

    def procBs(self):

        if self.curr_token.value == 'not':
            self.read()
            self.procBp()
            self.buildTree("not", 1)
        else:
            self.procBp()

    def procBp(self):

        self.procA()
        match self.curr_token.value:
            case '>':
                self.read()
                self.procA()
                self.buildTree("gr", 2)
            case 'gr':
                self.read()
                self.procA()
                self.buildTree("gr", 2)

            case 'ge':
                self.read()
                self.procA()
                self.buildTree("ge", 2)

            case '>=':
                self.read()
                self.procA()
                self.buildTree("ge", 2)



            case '<':
                self.read()
                self.procA()
                self.buildTree("ls", 2)

            case 'ls':
                self.read()
                self.procA()
                self.buildTree("ls", 2)

            case '<=':
                self.read()
                self.procA()
                self.buildTree("le", 2)

            case 'le':
                self.read()
                self.procA()
                self.buildTree("le", 2)

            case 'eq':
                self.read()
                self.procA()
                self.buildTree("eq", 2)

            case 'ne':
                self.read()
                self.procA()
                self.buildTree("ne", 2)

            case _:
                return

    def procA(self):
        if self.curr_token.value == '+':
            self.read()
            self.procAt()

        elif self.curr_token.value == '-':
            self.read()
            self.procAt()
            self.buildTree("neg", 1)


        else:
            self.procAt()
        plus = '+'
        while self.curr_token.value == '+' or self.curr_token.value == '-':

            if self.curr_token.value=='-':
                plus='-'

            self.read()
            self.procAt()
            self.buildTree(plus, 2)


    def procAt(self):
        self.procAf()

        while self.curr_token.value == '*' or self.curr_token.value == '/':
            self.read()
            self.procAf()
            self.buildTree("*", 2)

    def procAf(self):

        self.procAp()
        while self.curr_token.value == '**':
            self.read()
            self.procAf()
            self.buildTree("**", 2)

    def procAp(self):

        self.procR()
        while self.curr_token.value == '@':
            self.read()
            self.procR()
            self.buildTree("@", 2)

    def procR(self):

        self.procRn()
        while (self.curr_token.type in [Scanner.Type.ID, Scanner.Type.INT,Scanner.Type.STRING] or self.curr_token.value in ['true', 'false', 'nil', 'dummy', "("]):
            if self.index >= len(self.tokens):
                break
            self.procRn()
            self.buildTree("gamma", 2)

    def procRn(self):

        if self.curr_token.type in [Scanner.Type.ID, Scanner.Type.INT,
                                       Scanner.Type.STRING]:


            self.read()
        elif self.curr_token.value in ['true', 'false', 'nil', 'dummy']:
            self.read()
        elif self.curr_token.value == '(':
            self.read()
            self.procE()
            if self.curr_token.value != ')':
                return
            self.read()


    def procD(self):

        self.procDa()
        while self.curr_token.value == 'within':
            self.read()
            self.procD()
            self.buildTree("within", 2)

    def procDa(self):
        self.procDr()
        n = 0
        while self.curr_token.value == 'and':
            n += 1
            self.read()
            self.procDa()
        if n > 0:
            self.buildTree("and", n + 1)

    def procDr(self):

        if self.curr_token.value == 'rec':
            self.read()
            self.procDb()
            self.buildTree("rec", 1)

        self.procDb()

    def procDb(self):

        if self.curr_token.value == '(':
            self.read()
            self.procD()
            if self.curr_token.value != ')':
                return
            self.read()
            self.buildTree("()", 1)

        elif self.curr_token.type == Scanner.Type.ID:
            self.read()

            if self.curr_token.type == Scanner.Type.COMMA:
                self.read()
                self.procVb()

                if self.curr_token.value != '=':
                    print("Error: = is expected")
                    return
                self.buildTree(",", 2)
                self.read()
                self.procE()
                self.buildTree("=", 2)
            else :
                if self.curr_token.value == '=':
                    self.read()
                    self.procE()
                    self.buildTree("=", 2)

                else :

                    n = 0
                    while self.curr_token.type == Scanner.Type.ID or self.curr_token.value == '(':
                        self.procVb()
                        n += 1

                    if n == 0:
                        print("Error: ID or ( is expected")
                        return

                    if self.curr_token.value != '=':
                        print("Error: = is expected")
                        return
                    self.read()
                    self.procE()
                    self.buildTree("function_form", n + 2)


    def procVb(self):
        if self.curr_token.type == Scanner.Type.ID:
            self.read()

        elif self.curr_token.value == '(':
            self.read()
            if self.curr_token.type == ')':
                self.buildTree("()", 0)
                self.read()
            else:
                self.procVL()
                if self.curr_token.value != ')':
                    print("Error: ) is expected")
                    return
            self.read()

        else:
            print("Error: ID or ( is expected")
            return

    def procVL(self):

        if self.curr_token.type != Scanner.Type.ID:
            pass
        else:
            pass

            self.read()
            trees_to_pop = 0
            while self.curr_token.value == ',':
                self.read()
                if self.curr_token.type != Scanner.Type.ID:
                    print(" 572 VL: Identifier expected") 
                self.read()

                trees_to_pop += 1
            if trees_to_pop > 0:
                self.buildTree(',', trees_to_pop +1) 





# The main program

if len(sys.argv) > 1:
    argv_idx = 1  
    ast_flag = 0  

    if len(sys.argv) == 3:  # Check for the AST flag and print the AST
        argv_idx = 2
        if sys.argv[2] == "-ast": 
            ast_flag = 1

        input_path = sys.argv[1]  # Get the path to infut file as the 2nd argument
    else:
        input_path = sys.argv[1]

numeric_result_file=["test_cases/standarizer","test_cases/sum"]
test_results=[]
test_id=0


with open(input_path) as file:
    program = file.read()

stack = []
tokens = []


# Tokenize input using scanner
tokenizer = Scanner.Tokenizer(program)
token = tokenizer.next_token()
while token.type != Scanner.Type.EOF:
    tokens.append(token)
    token = tokenizer.next_token()

# Screening
screener = Screener(tokens)
tokens = screener.screen()

# Parsing
parser = Parser()
parser.tokens = tokens
parser.curr_token = tokens[0]
parser.index = 0

parser.procE()
root = stack[0]


root.indentation = 0
if ast_flag == 1: 
    root.print_tree_to_cmd()  # Printing AST if the ast flag is present


if ast_flag == 0:
    ASTStandarizer = ASTNode("ASTStandarizer")
    root= ASTStandarizer.standarize(root)

    ctrlStructGen = controlStructure.ControlStructureGenerator()
    ctr_structures=ctrlStructGen.generate_control_structures(root)

    cseMachine= CSEMachine(ctr_structures ,input_path)
    result=cseMachine.executeCSEMachine()

    for t in test_results:
        id+=1