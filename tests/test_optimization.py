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
    '''
    l1    x = 2 
                        defined = (x)
                        unused = {x: l1}
    l2    y = 1 + 4 
                        defined = (x, y)
                        unused = {x: l1, y: l2}
    l3    z = y - 2
                        defined = (x, y, z)
                        unused = {x: l1, z: l3}
    l4    x = z
                        defined = (x, y, z)
                        unused = {x: l4}
                        nodes_to_remove = (l1)

    '''
    lines1 = [optimize.Command('STORE', operand1=2, target='cat'),
             optimize.Command('ADD', operand1=1, operand2=2, target='dog'),
             optimize.Command('MOVE', operand1='dog', target='cat')]

    lines2 = [optimize.Command('ADD', operand1=1, operand2=2, target='dog'),
              optimize.Command('MOVE', operand1='dog', target='cat')]

    code_block = optimize.Block(lines1)
    code_block.eliminate_dead_code()
    
    assert code_block == optimize.Block(lines2)




