# calculator.py
import sys

print('Python Version: ' + sys.version)

# token types
#
# EOF (end-of-file): used to indicate no more input left for lexical analysis
INTEGER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EOF'

class Token(object):
    def __init__(self, type_, value):
        # token types: INTEGER, PLUS, MINUS, or EOF
        self.type_ = type_

        #token values: non-negative integers, '+', '-', or None
        self.value = value

    def __str__(self):
        '''
        Token(INTEGER, 3)
        Token(PLUS, '+')
        '''

        return 'Token({type_}, {value})'.format(type_ = self.type_, value = repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # string input
        self.text = text

        # index in text
        self.pos = 0

        # current token
        self.current_token = None

        # current character
        self.current_char = self.text[self.pos]

    # ---------------------------------------------------
    # Lexer
    # ---------------------------------------------------
    def error(self): raise Exception('Error parsing input.')

    def increment(self):
        '''
        Increment index in text and set current character.
        '''

        self.pos += 1
        if (self.pos > len(self.text) - 1):
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
        Return multi-digit integers.
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

            self.error()

        return Token(EOF, None)

    # ---------------------------------------------------
    # Parser (Interpreter)
    # ---------------------------------------------------
    def eat(self, token_type):
        '''
        Eat current token if match with passed token type.
        '''

        if (self.current_token.type_ == token_type):
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        '''
        Return integer token value.
        '''

        token = self.current_token
        self.eat(INTEGER)

        return token.value

    def expression(self):
        '''
        Arithmetic expression parser and interpreter.
        
        INTEGER PLUS INTEGER
        INTEGER MINUS INTEGER PLUS INTEGER
        '''

        # set current token to first token from input
        self.current_token = self.get_next_token()

        result = self.term()
        while (self.current_token.type_ in (PLUS, MINUS, MULTIPLY, DIVIDE)):
            token = self.current_token
            
            # plus
            if (token.type_ == PLUS):
                self.eat(PLUS)
                result = result + self.term()
            
            # minus
            elif (token.type_ == MINUS):
                self.eat(MINUS)
                result = result - self.term()

            # multiply
            elif (token.type_ == MULTIPLY):
                self.eat(MULTIPLY)
                result = result * self.term()

            # divide
            elif (token.type_ == DIVIDE):
                self.eat(DIVIDE)
                term = self.term()

                if (term > 0):
                    result = result / term
                else:
                    raise Exception('Zero divison error.')

        return result

def main():
    while True:
        try:
            text = input('calculator> ')

        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expression()
        
        print(result)

if (__name__ == '__main__'): main()





