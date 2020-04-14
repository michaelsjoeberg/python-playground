from spi import Lexer
from spi import Parser
from spi import Interpreter

#lexer = Lexer('5 + 5')
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())

# ---------------------------------------------------
# Asserts
# ---------------------------------------------------
#Interpreter(Parser(Lexer(text))).interpret()

assert (Interpreter(Parser(Lexer('7 + 3 * (10 / (12 / (3 + 1) - 1))'))).interpret() == 22)
assert (Interpreter(Parser(Lexer('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)'))).interpret() == 10)
assert (Interpreter(Parser(Lexer('7 + (((3 + 2)))'))).interpret() == 12)

# negation
assert (Interpreter(Parser(Lexer('- 3'))).interpret() == -3)
assert (Interpreter(Parser(Lexer('+ 3'))).interpret() == 3)
assert (Interpreter(Parser(Lexer('5 - - - + - 3'))).interpret() == 8)
assert (Interpreter(Parser(Lexer('5 - - - + - (3 + 4) - + 2'))).interpret() == 10)
