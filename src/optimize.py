class Block():
    '''
    Node of CFG. A linked-list of code commands within the same control block

    Between blocks: Do liveness analysis for dead-code elimination and register allocation 
    '''
    def __init__(self, commands, live_in=set()):
        self.head = None
        self.commands = commands

        # build linked-list
        if self.commands is not None:
            node = Node(self.commands.pop(0))
            self.head = node
            for command in self.commands:
                node.next = Node(command)
                node = node.next

        # would use these if had branches
        self.live_in = live_in
        self.used = set()
        self.defined = set()
        self.live_out = set()

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.command))
            node = node.next

        return " \n | \n | \n v \n ".join(nodes)

    def track_defined_variables(self):
        # for node in self:
        pass




class Node():
    '''
    Code lines/nodes WITHIN a Block

    '''
    def __init__(self, command, defined=set(), unused=set(), nodes_to_remove=set()):
        self.command = command
        self.next = None

        # keep track of the state of variables at each node in the block
        self.defined = defined
        self.unused = unused
        self.nodes_to_remove = nodes_to_remove

    def __repr__(self):
        return str(self.command)

    def __eq__(self, other):
        return (isinstance(self, other.__class__)) and (self.command == other.command)


class Command():
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

