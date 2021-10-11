from grammar import SyntaxChecker
'''
a := assignment | equation

assignment := constant EQUALS term
equation := constant EQUALS term op term

term := int_literal | constant
constant := DOLAR name
name := [a-zA-Z]+
int_literal := [0-9]+
op := '+' | '-'

'''

class Parser():

    def __init__(self, token_sequence):
        self.token_sequence = token_sequence

        self.asts = []
        self.syntax = SyntaxChecker()
        self.parsing_idx = 0

    def parse(self):
        while self.token_sequence[self.parsing_idx].type != 'EOF':
            self._parse_a()


    def _parse_a(self):
        tokens = self.token_sequence[self.parsing_idx:]

        if self.syntax.match_grammar_a(tokens):
            if self.syntax.match_grammar_assignment(tokens):
                self._parse_assignment(self, tokens)
            elif self.syntax.match_grammar_equation(tokens):
                self._parse_equation(self, tokens)
            else:
                raise SyntaxError(f"Line: {tokens[0].line_num}, Must be assignment or equation")
        else:
            raise SyntaxError(f"Line: {tokens[0].line_num}, Need 'constant EQUALS'")

    def _parse_assignment(self, tokens):
        pass

    def _parse_equation(self, tokens):
        pass
        
