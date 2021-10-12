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

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __eq__(self, other):
        return (isinstance(self, other.__class__)) and (self.head == other.head)



    def _assess_liveness(self):
        for node in self:
            oprnd1 = node.command.operand1
            oprnd2 = node.command.operand2
            target = node.command.target
            node_num = node.command.node_num

            # update variables defined
            self.defined.add(target)
            self.unused[target] = node_num

            # update what variables have been used in block
            if oprnd1 is not None and oprnd1 in self.unused:
                del self.unused[oprnd1]
            if oprnd2 is not None and oprnd2 in self.unused:
                del self.unused[oprnd1]

    def syntax_check(self):
        # determine if variable used before defined
        for node in self:
            oprnd1 = node.command.operand1
            oprnd2 = node.command.operand2
            target = node.command.target
            node_num = node.command.node_num

            if (oprnd1 is not None) and (oprnd1 not in self.defined):
                raise Exception(f'{oprnd1} on line {node_num} not defined')

            if (oprnd2 is not None) and (oprnd2 not in self.defined):
                raise Exception(f'{oprnd2} on line {node_num} not defined')



    def remove_node(self, node_num):
        if self.head is None:
            raise Exception('Block is empty')

        if self.head.command.node_num == node_num:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.command.node_num == node_num:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception(f'{node_num} not found')



    def _find_dead_code(self):
        self._assess_liveness()
        for node in self:
            oprnd1 = node.command.operand1
            oprnd2 = node.command.operand2
            target = node.command.target

            if (target is not None) and (target in self.unused):
                node_to_remove = self.unused.pop(target)
                self.nodes_to_remove.add(node_to_remove)

    def eliminate_dead_code(self):
        self._find_dead_code()
        print('nodes to remove', self.nodes_to_remove)
        for node_num in self.nodes_to_remove:
            self.remove_node(node_num)



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
        return ((isinstance(self, other.__class__)) and (self.command == other.command) 
            and (self.next == other.next))


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
    def __init__(self, type_, operand1=None, operand2=None, target=None, node_num=None):
        self.type_ = type_
        self.operand1 = operand1
        self.operand2 = operand2
        self.target = target
        self.node_num = node_num

    def __repr__(self):
        return f'{self.type_}({self.operand1}, {self.operand2} -> {self.target})'

    def __eq__(self, other):
        return (isinstance(self, other.__class__)
                and (self.type_ == other.type_)
                and (self.operand1 == other.operand1)
                and (self.operand2 == other.operand2)
                and (self.target == other.target))

