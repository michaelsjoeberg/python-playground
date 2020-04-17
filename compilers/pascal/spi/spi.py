# Recursive descent parser: https://en.wikipedia.org/wiki/Recursive_descent_parser
import sys
print('Python Version: ' + sys.version)

# https://ruslanspivak.com/lsbasi-part1/
# https://github.com/rspivak/lsbasi/blob/master/part7/rust/spi/src/main.rs

'''
    Context-free grammars (Backus-Naur Form)

    program                 : PROGRAM variable SEMI block DOT
    block                   : declarations compound_statement
    declarations            : VAR (variable_declaration SEMI)+ | empty
    variable_declaration    : ID (COMMA ID)* COLON type_spec
    type_spec               : INTEGER | REAL
    compound_statement      : BEGIN statement_list END
    statement_list          : statement | statement SEMI statement_list
    statement               : compound_statement | assignment_statement | empty
    assignment_statement    : variable ASSIGN expr
    empty                   : 
    expr                    : term ((PLUS | MINUS) term)*
    term                    : factor ((MULTIPLY | INTEGER_DIV | FLOAT_DIV) factor)*
    factor                  : PLUS factor | MINUS factor | INTEGER_CONST | REAL_CONST | LPAR expr RPAR | variable
    variable                : ID
'''

# ---------------------------------------------------
# Lexer : Generate tokens
# ---------------------------------------------------
INTEGER       = 'INTEGER'
REAL          = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST    = 'REAL_CONST'
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MULTIPLY      = 'MULTIPLY'
INTEGER_DIV   = 'INTEGER_DIV'
FLOAT_DIV     = 'FLOAT_DIV'
LPAR          = 'LPAR'
RPAR          = 'RPAR'
ID            = 'ID'
ASSIGN        = 'ASSIGN'
BEGIN         = 'BEGIN'
END           = 'END'
SEMI          = 'SEMI'
DOT           = 'DOT'
PROGRAM       = 'PROGRAM'
VAR           = 'VAR'
COLON         = 'COLON'
COMMA         = 'COMMA'
EOF           = 'EOF'

class Token(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        '''
        String representation of class instance.
        
            Token(INTEGER_CONST, 3)
            Token(PLUS, '+')
            Token(MULTIPLY, '*')
        '''

        return 'Token({type_}, {value})'.format(
            type_ = self.type_,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END')
}

class Lexer(object):
    def __init__(self, text):
        self.text = text

        # index in text
        self.pos = 0

        # current character
        self.current_char = self.text[self.pos]

    def error(self): raise Exception('Invalid character.')

    def increment(self):
        '''
        Increment index in text and set current character.
        '''
        self.pos += 1
        
        if (self.pos > len(self.text) - 1):
            # end of input
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1

        if (peek_pos > len(self.text) - 1):
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while (self.current_char is not None and self.current_char.isspace()):
            self.increment()

    def skip_comment(self):
        while (self.current_char != '}'):
            self.increment()

        # closing curly brace
        self.increment()

    def number(self):
        '''
        Return integer or float.
        '''
        result = ''
        
        while (self.current_char is not None and self.current_char.isdigit()):
            result += self.current_char
            self.increment()

        if (self.current_char == '.'):
            result += self.current_char
            self.increment()

            while (self.current_char is not None and self.current_char.isdigit()):
                result += self.current_char
                self.increment()

            token = Token('REAL_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))

        return token

    def _id(self):
        '''
        Handle identifiers and reserved keywords.
        '''
        result = ''

        while (self.current_char is not None and self.current_char.isalnum()):
            result += self.current_char
            self.increment()

        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result.lower()))
        #token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    # lexical analyzer (tokenizer)
    def get_next_token(self):
        '''
        Break input into tokens.
        '''

        while (self.current_char is not None):

            # whitespace (skip)
            if (self.current_char.isspace()):
                self.skip_whitespace()
                continue

            # comment
            if (self.current_char == '{'):
                self.increment()
                self.skip_comment()
                continue

            # ID
            if (self.current_char.isalpha()):
                return self._id()

            # INTEGER FLOAT
            if (self.current_char.isdigit()):
                return self.number()

            # ASSIGN
            if (self.current_char == ':' and self.peek() == '='):
                self.increment()
                self.increment()
                return Token(ASSIGN, ':=')

            # SEMI
            if (self.current_char == ';'):
                self.increment()
                return Token(SEMI, ';')

            # COLON
            if (self.current_char == ':'):
                self.increment()
                return Token(COLON, ':')

            # COMMA
            if (self.current_char == ','):
                self.increment()
                return Token(COMMA, ',')

            # PLUS
            if (self.current_char == '+'):
                self.increment()
                return Token(PLUS, '+')

            # MINUS
            if (self.current_char == '-'):
                self.increment()
                return Token(MINUS, '-')

            # MULTIPLY
            if (self.current_char == '*'):
                self.increment()
                return Token(MULTIPLY, '*')

            # FLOAT_DIV
            if (self.current_char == '/'):
                self.increment()
                return Token(FLOAT_DIV, '/')

            # LPAR
            if (self.current_char == '('):
                self.increment()
                return Token(LPAR, '(')

            # RPAR
            if (self.current_char == ')'):
                self.increment()
                return Token(RPAR, ')')

            # DOT
            if (self.current_char == '.'):
                self.increment()
                return Token(DOT, '.')

            self.error()

        return Token(EOF, None)

# ---------------------------------------------------
# Parser : Build AST (using tokens)
# ---------------------------------------------------
class AST(object): pass

class Compound(AST):
    '''
    Represent 'BEGIN ... END' block.
    '''

    def __init__(self): self.children = []

class Assign(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = operator
        self.operator = operator
        self.right = right

class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Empty(AST): pass

class BinaryOperator(AST):
    def __init__(self, left, operator, right):
        '''
        BinaryOperator('+'):
            BinaryOperator('*'):
                Number(2)
                Number(7)
            Number(3)
        '''

        self.left = left
        self.token = operator
        self.operator = operator
        self.right = right

class UnaryOperator(AST):
    def __init__(self, operator, expr):
        self.token = operator
        self.operator = operator
        self.expr = expr

class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Program(AST):
    '''
    Root node.
    '''

    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VariableDeclaration(AST):
    def __init__(self, variable_node, type_node):
        self.variable_node = variable_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer

        # set current token to first token from input
        self.current_token = self.lexer.get_next_token()

    def error(self): raise Exception('Invalid syntax.')

    def eat(self, token_type):
        '''
        Eat current token if match with passed token type.
        '''

        if (self.current_token.type_ == token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        '''
        program : PROGRAM variable SEMI block DOT
        '''
        self.eat(PROGRAM)
        
        variable_node = self.variable()
        program_name = variable_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(program_name, block_node)
        self.eat(DOT)

        return program_node

    def block(self):
        '''
        block : declarations compound_statement
        '''

        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()

        node = Block(declaration_nodes, compound_statement_node)

        return node

    def declarations(self):
        '''
        declarations : VAR (variable_declaration SEMI)+ | empty
        '''
        declarations = []

        if (self.current_token.type_ == VAR):
            self.eat(VAR)

            while (self.current_token.type_ == ID):
                variable_declaration = self.variable_declaration()
                declarations.extend(variable_declaration)
                self.eat(SEMI)

        return declarations

    def variable_declaration(self):
        '''
        variable_declaration : ID (COMMA ID)* COLON type_spec
        '''

        # first ID
        variable_nodes = [Variable(self.current_token)]
        self.eat(ID)

        while (self.current_token.type_ == COMMA):
            self.eat(COMMA)
            variable_nodes.append(Variable(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        variable_declarations = [
            VariableDeclaration(variable_node, type_node)
            for variable_node in variable_nodes
        ]

        return variable_declarations

    def type_spec(self):
        '''
        type_spec : INTEGER | REAL
        '''
        token = self.current_token

        if (self.current_token.type_ == INTEGER):
            self.eat(INTEGER)
        else:
            self.eat(REAL)

        node = Type(token)

        return node

    def compound_statement(self):
        '''
        compound_statement : BEGIN statement_list END
        '''

        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        '''
        statement_list : statement | statement SEMI statement_list
        '''

        node = self.statement()

        results = [node]

        while (self.current_token.type_ == SEMI):
            self.eat(SEMI)
            results.append(self.statement())

        # if (self.current_token.type_ == ID):
        #     self.error()

        return results

    def statement(self):
        '''
        statement : compound_statement | assignment_statement | empty
        '''

        if (self.current_token.type_ == BEGIN):
            node = self.compound_statement()

        elif (self.current_token.type_ == ID):
            node = self.assignment_statement()

        else:
            node = self.empty()

        return node

    def assignment_statement(self):
        '''
        assignment_statement : variable ASSIGN expr
        '''

        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def variable(self):
        '''
        variable : ID
        '''

        node = Variable(self.current_token)
        self.eat(ID)

        return node

    def empty(self): return Empty()

    def factor(self):
        '''
        factor : PLUS factor | MINUS factor | INTEGER_CONST | REAL_CONST | LPAR expr RPAR | variable
        '''
        token = self.current_token

        # PLUS
        if (token.type_ == PLUS):
            self.eat(PLUS)
            node = UnaryOperator(token, self.factor())
            return node

        # MINUS
        elif (token.type_ == MINUS):
            self.eat(MINUS)
            node = UnaryOperator(token, self.factor())
            return node

        # INTEGER_CONST
        elif (token.type_ == INTEGER_CONST):
            self.eat(INTEGER_CONST)
            return Number(token)

        # REAL_CONST 
        elif (token.type_ == REAL_CONST):
            self.eat(REAL_CONST)
            return Number(token)
        
        # LPAR expr LPAR
        elif (token.type_ == LPAR):
            self.eat(LPAR)
            node = self.expr()
            self.eat(RPAR)
            return node

        else:
            node = self.variable()
            return node

    def term(self):
        '''
        term : factor ((MULTIPLY | INTEGER_DIV | FLOAT_DIV) factor)*
        '''
        node = self.factor()
        
        while (self.current_token.type_ in (MULTIPLY, INTEGER_DIV, FLOAT_DIV)):
            token = self.current_token

            # MULTIPLY
            if (token.type_ == MULTIPLY)        : self.eat(MULTIPLY)
            # INTEGER_DIV
            elif (token.type_ == INTEGER_DIV)   : self.eat(INTEGER_DIV)
            # FLOAT_DIV
            elif (token.type_ == FLOAT_DIV)     : self.eat(FLOAT_DIV)

            node = BinaryOperator(left=node, operator=token, right=self.factor())

        return node

    def expr(self):
        '''
        Arithmetic expression parser.
        
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAR expr RPAR
        '''
        node = self.term()
        
        while (self.current_token.type_ in (PLUS, MINUS)):
            token = self.current_token
            
            # PLUS
            if (token.type_ == PLUS):
                self.eat(PLUS)
            
            # MINUS
            elif (token.type_ == MINUS):
                self.eat(MINUS)

            node = BinaryOperator(left=node, operator=token, right=self.term())

        return node

    # syntax analyzer
    def parse(self):
        node = self.program()

        if (self.current_token.type_ != EOF):
            self.error()

        return node

# ---------------------------------------------------
# Interpreter : Execute instructions in AST
# ---------------------------------------------------
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)

        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_Program(self, node):

        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)

    def visit_VariableDeclaration(self, node): pass

    def visit_Type(self, node): pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Empty(self, node): pass

    def visit_Assign(self, node):
        variable_name = node.left.value

        # variable name and value assigned to variable
        # GLOBAL_SCOPE is symbol table
        self.GLOBAL_SCOPE[variable_name] = self.visit(node.right)

    def visit_Variable(self, node):
        variable_name = node.value
        variable_value = self.GLOBAL_SCOPE.get(variable_name)

        if (variable_value is None):
            raise NameError(repr(variable_name))
        else:
            return variable_value

    def visit_BinaryOperator(self, node):
        # PLUS
        if (node.operator.type_ == PLUS):
            return self.visit(node.left) + self.visit(node.right)
        # MINUS
        elif (node.operator.type_ == MINUS):
            return self.visit(node.left) - self.visit(node.right)
        # MULTIPLY
        elif (node.operator.type_ == MULTIPLY):
            return self.visit(node.left) * self.visit(node.right)
        # INTEGER_DIV
        elif (node.operator.type_ == INTEGER_DIV):
            return self.visit(node.left) // self.visit(node.right)
        # FLOAT_DIV
        elif (node.operator.type_ == FLOAT_DIV):
            return float(self.visit(node.left) / self.visit(node.right))

    def visit_UnaryOperator(self, node):
        # PLUS
        if (node.operator.type_ == PLUS):
            return +self.visit(node.expr)
        # MINUS
        elif (node.operator.type_ == MINUS):
            return -self.visit(node.expr)

    def visit_Number(self, node):
        
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        if (tree is None):
            return ''

        return self.visit(tree)

def main():
    while True:
        try:
            text = input('calculator> ')

        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        
        print(result)

if (__name__ == '__main__'): main()





