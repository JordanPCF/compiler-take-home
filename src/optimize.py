class Block():
    '''
    Node of CFG. A linked-list of code commands within the same control block

    Between blocks: Do liveness analysis for dead-code elimination and register allocation 
    '''
    def __init__(self, commands, live_in=set()):
        self.head = None
        self.commands = commands

        # keep track of the state of variables at each node in the block
        self.defined = set()
        self.unused = dict()
        self.nodes_to_remove = set()

        # would use these if had control branches
        self.live_in = live_in
        self.live_out = set()

        # build linked-list
        if self.commands is not None:
            node = Node(self.commands.pop(0))
            self.head = node
            for command in self.commands:
                node.next = Node(command)
                node = node.next


    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.command))
            node = node.next

        return " \n | \n | \n v \n ".join(nodes)


class Node():
    '''
    Code lines/nodes WITHIN a Block

    '''
    def __init__(self, command):
        self.command = command
        self.next = None


    def __repr__(self):
        return str(self.command)

    def __eq__(self, other):
        return (isinstance(self, other.__class__)) and (self.command == other.command)


class Command():
    '''
    Intermediate Representation

    properties:
    type_: STORE, ADD, SUBTRACT, MOVE, EOF

    e.g.
    $cat = 2         ---->    Command('STORE', operand1=2, target='cat')
    $cat = 2 + 10    ---->    Command('ADD', operand1=2, operand2=10, target='cat')
    $cat = 2 - 10    ---->    Command('SUBTRACT', operand1=2, operand2=10, target='cat')
    $dog = $cat      ---->    Command('MOVE', operand1=cat, target='dog')
                              Command('EOF')

    '''
    def __init__(self, type_, operand1=None, operand2=None, target=None):
        self.type_ = type_
        self.operand1 = operand1
        self.operand2 = operand2
        self.target = target

    def __repr__(self):
        return f'{self.type_}({self.operand1}, {self.operand2} -> {self.target})'

    def __eq__(self, other):
        return (isinstance(self, other.__class__)
                and (self.type_ == other.type_)
                and (self.operand1 == other.operand1)
                and (self.operand2 == other.operand2)
                and (self.target == other.target))

