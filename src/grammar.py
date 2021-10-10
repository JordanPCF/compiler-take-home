class SyntaxChecker():

    def __init__(self):
        pass

    def match_grammar_a(self, tokens):
        return ((len(tokens) > 3)
               and (tokens[0].type == 'constant')
               and (tokens[1].type == 'EQUALS'))