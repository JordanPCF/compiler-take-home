import pytest
from compiler.src import optimize




def test_chain_commands():
    '''
    txt file: 

    $cat = 2
    $dog = 1 + 2

    STORE(2, cat)
        |
        |
        v
    ADD(1, 2, dog)
    '''
    lines = [optimize.Command('STORE', operand1=2, target='cat'),
             optimize.Command('ADD', operand1=1, operand2=2, target='dog')]

    code_block = optimize.Block(lines)

    assert ((code_block.head == optimize.Node(
                                    optimize.Command('STORE', operand1=2, target='cat'))) 
        and (code_block.head.next == optimize.Node(
                                    optimize.Command('ADD', operand1=1, operand2=2, target='dog'))))

def test_constants_declared_before_use():
    pass

def test_constant_folding():
    pass

def test_remove_identity_lines():
    pass

def test_constant_propagation():
    pass

def test_dead_code_elimination():
    pass



