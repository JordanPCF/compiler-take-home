import tokenize as tkn

class Token():
    def __init__(self, type_, value, line_num=1):
        self.type_ = type_
        self.value = value
        self.line_num = line_num

    def __repr__(self):
        return f"Token({self.type_}, '{self.value}')"

    def __eq__(self, other):
        return (isinstance(self, other.__class__)
                and (self.type_ == other.type_)
                and (self.value == other.value))


def tokenize(file_name):
    tokens = _get_tokens(file_name)
    transformed_tokens = _transform_tokens(tokens)

    return transformed_tokens

def _get_tokens(file_name):
    with tkn.open(file_name) as f:
        return list(tkn.generate_tokens(f.readline))

def _transform_tokens(tokens):
    transformed_tokens = []

    for token in list(tokens):
        transformed_tokens.append(Token('constant', 'cat', 1))

    return transformed_tokens