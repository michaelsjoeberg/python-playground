# https://ruslanspivak.com/lsbasi-part4/
from calculator import Lexer
from calculator import Interpreter

#lexer = Lexer('5 + 5')
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())

# ---------------------------------------------------
# Asserts
# ---------------------------------------------------
assert (Interpreter(Lexer('3')).expr() == 3)
assert (Interpreter(Lexer('2 + 7 * 4')).expr() == 30)
assert (Interpreter(Lexer('7 - 8 / 4')).expr() == 5)
assert (Interpreter(Lexer('14 + 2 * 3 - 6 / 2')).expr() == 17)