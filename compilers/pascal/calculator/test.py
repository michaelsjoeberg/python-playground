from calculator import Lexer
from calculator import Parser
from calculator import Interpreter

#lexer = Lexer('5 + 5')
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())
# print(lexer.get_next_token())

# ---------------------------------------------------
# Asserts
# ---------------------------------------------------
assert (Interpreter(Parser(Lexer('7 + 3 * (10 / (12 / (3 + 1) - 1))'))).interpret() == 22)
assert (Interpreter(Parser(Lexer('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)'))).interpret() == 10)
assert (Interpreter(Parser(Lexer('7 + (((3 + 2)))'))).interpret() == 12)
