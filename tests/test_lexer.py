import pytest
import tokenize as tkn
from io import BytesIO
from compiler.src import lexer

def test_transform_constants():
    text = "$cat"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('constant', 'cat'),
                           lexer.Token('EOF', '')]


def test_transform_ints():
    text = "123"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('int_literal', 123),
                           lexer.Token('EOF', '')]

def test_transform_addition():
    text = "1 + 2"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('int_literal', 1),
                           lexer.Token('op', '+'),
                           lexer.Token('int_literal', 2),
                           lexer.Token('EOF', '')]

def test_transform_subtraction():
    text = "1 - 2"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('int_literal', 1),
                           lexer.Token('op', '-'),
                           lexer.Token('int_literal', 2),
                           lexer.Token('EOF', '')]

def test_transform_assignment():
    text = "$cat = 2"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('constant', 'cat'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('int_literal', 2),
                           lexer.Token('EOF', '')]

def test_transform_equation():
    text = "$meow = $cat - $dog"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('constant', 'meow'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('constant', 'cat'),
                           lexer.Token('op', '-'),
                           lexer.Token('constant', 'dog'),
                           lexer.Token('EOF', '')]

def test_transform_multiple_lines():
    text = "$cat = 2 \n $dog = 9\n $meow = $cat - $dog \n \n$woof = $dog + 10"
    transformed = lexer._transform_tokens(_tokenize(text))

    assert transformed == [lexer.Token('constant', 'cat'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('int_literal', 2),
                           lexer.Token('NEWLINE', '\\n'),
                           lexer.Token('constant', 'dog'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('int_literal', 9),
                           lexer.Token('NEWLINE', '\\n'),
                           lexer.Token('constant', 'meow'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('constant', 'cat'),
                           lexer.Token('op', '-'),
                           lexer.Token('constant', 'dog'),
                           lexer.Token('NEWLINE', '\\n'),
                           lexer.Token('NEWLINE', '\\n'),
                           lexer.Token('constant', 'woof'),
                           lexer.Token('EQUALS', '='),
                           lexer.Token('constant', 'dog'),
                           lexer.Token('op', '+'),
                           lexer.Token('int_literal', 10),
                           lexer.Token('EOF', '')]

def _tokenize(text):
    return list(tkn.tokenize(BytesIO(text.encode('utf-8')).readline))

