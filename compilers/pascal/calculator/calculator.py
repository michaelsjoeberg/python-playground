# calculator.py
import sys
print('Python Version: ' + sys.version)

# Recursive descent parser: https://en.wikipedia.org/wiki/Recursive_descent_parser
# Based on https://ruslanspivak.com/lsbasi-part1/

# ---------------------------------------------------
# Lexer
# ---------------------------------------------------
# token types (note: EOF means no more input left for lexical analysis)
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAR, RPAR, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAR', 'RPAR', 'EOF'
)

class Token(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        '''
        Token(INTEGER, 3)
        Token(PLUS, '+')
        Token(MULTIPLY, '*')
        '''

        return 'Token({type_}, {value})'.format(
            type_ = self.type_,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

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

    def skip_whitespace(self):
        '''
        Skip whitespace.
        '''

        while (self.current_char is not None and self.current_char.isspace()):
            self.increment()

    def integer(self):
        '''
        Return a multi-digit integer.
        '''
        result = ''
        
        while (self.current_char is not None and self.current_char.isdigit()):
            result += self.current_char
            self.increment()

        return int(result)

    # Lexical Analyzer (Tokenizer)
    def get_next_token(self):
        '''
        Break input into tokens.
        '''

        while (self.current_char is not None):

            # whitespace
            if (self.current_char.isspace()):
                self.skip_whitespace()
                continue

            # multi-digit integers
            if (self.current_char.isdigit()):
                return Token(INTEGER, self.integer())

            # plus
            if (self.current_char == '+'):
                self.increment()
                return Token(PLUS, '+')

            # minus
            if (self.current_char == '-'):
                self.increment()
                return Token(MINUS, '-')

            # multiply
            if (self.current_char == '*'):
                self.increment()
                return Token(MULTIPLY, '*')

            # divide
            if (self.current_char == '/'):
                self.increment()
                return Token(DIVIDE, '/')

            # lpar
            if (self.current_char == '('):
                self.increment()
                return Token(LPAR, '(')

            # rpar
            if (self.current_char == ')'):
                self.increment()
                return Token(RPAR, ')')

            self.error()

        return Token(EOF, None)

# ---------------------------------------------------
# Parser
# ---------------------------------------------------
class AST(object): pass

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

class Number(AST):
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

    def factor(self):
        '''
        factor : INTEGER | LPAR expr RPAR
        '''
        token = self.current_token

        # INTEGER
        if (token.type_ == INTEGER):
            self.eat(INTEGER)
            
            return Number(token)
        
        # LPAR / LPAR
        elif (token.type_ == LPAR):
            self.eat(LPAR)
            node = self.expr()
            self.eat(RPAR)
            return node

    def term(self):
        '''
        term : factor ((MULTIPLY | DIVIDE) factor)*
        '''
        node = self.factor()
        
        while (self.current_token.type_ in (MULTIPLY, DIVIDE)):
            token = self.current_token

            # MULTIPLY
            if (token.type_ == MULTIPLY):
                self.eat(MULTIPLY)

            # DIVIDE
            elif (token.type_ == DIVIDE):
                self.eat(DIVIDE)

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

    def parse(self):
        return self.expr()

# ---------------------------------------------------
# Interpreter
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
        # DIVIDE
        elif (node.operator.type_ == DIVIDE):
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()

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





