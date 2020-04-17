# https://www.onlinegdb.com/online_pascal_compiler
from spi import Lexer
from spi import Parser
from spi import Interpreter

# lexer
# lexer = Lexer('BEGIN a := 2; END.')
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# Token(BEGIN, 'BEGIN')
# Token(ID, 'a')
# Token(ASSIGN, ':=')
# Token(INTEGER, 2)
# Token(SEMI, ';')
# Token(END, 'END')
# Token(DOT, '.')
# Token(EOF, None)

# parse file
with open('test_full.pas', 'r') as file:
	text = file.read()

	lexer = Lexer(text)
	parser = Parser(lexer)
	interpreter = Interpreter(parser)
	interpreter.interpret()

	for k, v in sorted(interpreter.GLOBAL_SCOPE.items()): print('{} = {}'.format(k, v))

# a = 2
# b = 25
# c = 27
# number = 2
# x = 11
# y = 5.997142857142857