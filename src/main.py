from parser import Parser
from lexer import tokenize

TEST_FILE = "test_program.txt"

parser = Parser(tokenize(TEST_FILE))

# print('here')
# parser.parse()

