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


def _tokenize(text):
    return list(tkn.tokenize(BytesIO(text.encode('utf-8')).readline))

