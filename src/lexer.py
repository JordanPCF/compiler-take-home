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


# tkn module's token type definition
TOKEN_TYPES = {
    'ERRORTOKEN': 59,
    'NAME': 1,
    'OP': 54,
    'NUMBER': 2,
    'NEWLINE': 4,
    'NL': 61,
    'ENDMARKER': 0,
    'ENCODING': 62,
    'INDENT': 5,
    'DEDENT': 6
}


def tokenize(file_name):
    ''' Generates tokens that match the grammar:

    constant ($[name])
    int_literal
    op (+/-)
    EQUALS

    Will use the lexing capabilities of the 'tokenize' package and then transform
    those tokens to the above forms
    '''
    tokens = _get_tokens(file_name)
    transformed_tokens = _transform_tokens(tokens)

    return transformed_tokens


def _get_tokens(file_name):
    with tkn.open(file_name) as f:
        return list(tkn.generate_tokens(f.readline))


def _transform_tokens(tokens):
    transformed_tokens = []
    token_idx = 0

    while token_idx < len(tokens) - 1:
        current_token = tokens[token_idx]
        current_token_type = _get_token_type(current_token)
        current_token_line_num = current_token.start[0]

        next_token = tokens[token_idx + 1]
        next_token_type = _get_token_type(next_token)

        if current_token_type == 'DOLLAR':
            if next_token_type == 'name':
                transformed_tokens.append(Token('constant',
                                                next_token.string,
                                                current_token_line_num))
                token_idx += 2
            else:
                raise SyntaxError("'$' must be followed by a constant name")

        elif current_token_type == 'EQUALS':
            transformed_tokens.append(Token('EQUALS',
                                            '=',
                                            current_token_line_num))  
            token_idx += 1

        elif current_token_type == 'int_literal':
            transformed_tokens.append(Token('int_literal',
                                            int(current_token.string),
                                            current_token_line_num))
            token_idx += 1

        elif current_token_type == 'op':
            transformed_tokens.append(Token('op',
                                            current_token.string,
                                            current_token_line_num))
            token_idx += 1

        elif current_token_type == 'encoding_info':
            # skip it
            token_idx += 1

        elif current_token_type == 'WHITESPACE':
            if next_token_type == 'EOF':
                transformed_tokens.append(Token('EOF',
                                                '',
                                                current_token_line_num))
                break
            else:
                # skip it
                token_idx += 1

        elif current_token_type == 'NEWLINE':
            if next_token_type == 'EOF':
                transformed_tokens.append(Token('EOF',
                                                '',
                                                current_token_line_num))
                break
            else:
                transformed_tokens.append(Token('NEWLINE',
                                                '\\n',
                                                current_token_line_num))
            token_idx += 1

        else:
            raise SyntaxError(f'Error reading token {current_token}')

    return transformed_tokens


def _get_token_type(token):
    token_type = ''

    if token.type == TOKEN_TYPES['ERRORTOKEN']:
        if token.string == '$':
            token_type = 'DOLLAR'
        elif token.string == ' ':
            token_type = 'WHITESPACE'

    elif token.type == TOKEN_TYPES['NAME']:
        token_type = 'name'

    elif token.type == TOKEN_TYPES['OP'] and token.string == '=':
        token_type = 'EQUALS'

    elif token.type == TOKEN_TYPES['OP'] and token.string == '+':
        token_type = 'op'

    elif token.type == TOKEN_TYPES['OP'] and token.string == '-':
        token_type = 'op'

    elif token.type == TOKEN_TYPES['NUMBER']:
        token_type = 'int_literal'

    elif token.type == TOKEN_TYPES['ENCODING']:
        token_type = 'encoding_info'

    elif token.type == TOKEN_TYPES['NEWLINE'] or token.type == TOKEN_TYPES['NL']:
        token_type = 'NEWLINE'

    elif token.type == TOKEN_TYPES['INDENT'] or token.type == TOKEN_TYPES['DEDENT']:
        token_type = 'WHITESPACE'

    elif token.type == TOKEN_TYPES['ENDMARKER']:
        token_type = 'EOF'

    return token_type

