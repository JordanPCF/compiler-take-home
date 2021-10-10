import pytest
import tokenize as tkn
from io import BytesIO
from compiler.src import lexer

def test_transform_constants():
    text = "$cat"
    tokens = tkn.tokenize(BytesIO(text.encode('utf-8')).readline)
    transformed = lexer._transform_tokens(tokens)

    assert transformed[0] == lexer.Token('constant', 'cat')
