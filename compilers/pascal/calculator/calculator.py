# calculator.py
import sys

print('Python Version: ' + sys.version)

# Recursive descent parser: https://en.wikipedia.org/wiki/Recursive_descent_parser
#
# Based on https://ruslanspivak.com/lsbasi-part1/

# token types
#
# EOF (end-of-file): no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAR, RPAR, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAR', 'RPAR', 'EOF'
)

class Token(object):
    def __init__(self, type_, value):
        # token types, e.g. INTEGER, PLUS, MINUS, or EOF
        self.type_ = type_

        #token values, e.g. non-negative integers, '+', '-', or None
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

# ---------------------------------------------------
# Lexer
# ---------------------------------------------------
class Lexer(object):
    def __init__(self, text):
        # string input
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

    def get_next_token(self):
        '''
        Lexical analyzer (tokenizer): break input into tokens.
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
# Interpreter
# ---------------------------------------------------
class Interpreter(object):
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

        # integer
        if (token.type_ == INTEGER):
            self.eat(INTEGER)
            return token.value
        
        # lpar / rpar
        elif (token.type_ == LPAR):
            self.eat(LPAR)
            result = self.expr()
            self.eat(RPAR)
            return result

    def term(self):
        '''
        term : factor ((MULTIPLY | DIVIDE) factor)*
        '''
        result = self.factor()
        
        while (self.current_token.type_ in (MULTIPLY, DIVIDE)):
            token = self.current_token

            # multiply
            if (token.type_ == MULTIPLY):
                self.eat(MULTIPLY)
                result = result * self.factor()

            # divide
            elif (token.type_ == DIVIDE):
                self.eat(DIVIDE)
                result = result / self.factor()
                
                # factor = self.factor()
                # if (factor > 0):
                #     result = result / factor
                # else:
                #     raise Exception('Zero divison error.')

        return result

    def expr(self):
        '''
        Arithmetic expression parser.
        
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAR expr RPAR
        '''
        result = self.term()
        
        while (self.current_token.type_ in (PLUS, MINUS)):
            token = self.current_token
            
            # plus
            if (token.type_ == PLUS):
                self.eat(PLUS)
                result = result + self.term()
            
            # minus
            elif (token.type_ == MINUS):
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = input('calculator> ')

        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        
        print(result)

if (__name__ == '__main__'): main()





