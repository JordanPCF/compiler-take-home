import pytest
from compiler.src import optimize




def test_chain_commands():
    '''
    txt file: 
    $cat = 2
    $dog = 1 + 2
    '''
    lines = [optimize.Command('STORE', operand1=2, target='cat'),
             optimize.Command('ADD', operand1=1, operand2=2, target='dog')]

    code_block = optimize.Block(lines)

    assert ((code_block.head == optimize.Node(
                                    optimize.Command('STORE', operand1=2, target='cat'))) 
        and (code_block.head.next == optimize.Node(
                                    optimize.Command('ADD', operand1=1, operand2=2, target='dog'))))


