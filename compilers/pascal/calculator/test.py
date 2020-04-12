# https://ruslanspivak.com/lsbasi-part4/
from calculator import Interpreter

interpreter = Interpreter('5 + 5')

print(interpreter.get_next_token())
print(interpreter.get_next_token())
print(interpreter.get_next_token())
print(interpreter.get_next_token())