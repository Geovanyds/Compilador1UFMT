from analisador_semantico import semantic


def fator(tokens):
    if tokens[0].tipo == 'real' or tokens[0].tipo == 'integer':
        semantic.append(tokens[0])
        semantic.insert(tokens[0].tipo.lower())
        semantic.check_type(tokens[0])
        tokens.pop(0)
    elif tokens[0].tipo == 'ident':
        semantic.search(tokens[0])
        semantic.check_type(tokens[0])
        tokens.pop(0)
    elif tokens[0].tipo == '(':
        tokens.pop(0)
        expressao(tokens)
        if tokens[0].tipo == ')':
            tokens.pop(0)
        else:
            raise SyntaxError('23')
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo identificador'.format(tokens[0].nome, tokens[0].line))


def op_mul(tokens):
    if tokens[0].tipo == '*' or tokens[0].tipo == '/':
        tokens.pop(0)
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo * ou /'.format(tokens[0].nome, tokens[0].line))


def mais_fatores(tokens):

    if tokens[0].tipo == '*' or tokens[0].tipo == '/':
        op_mul(tokens)
        fator(tokens)

        mais_fatores(tokens)
    else:
        pass


def termo(tokens):
    op_un(tokens)
    fator(tokens)
    mais_fatores(tokens)


def op_ad(tokens):
    if tokens[0].tipo == '+' or tokens[0].tipo == '-':
        tokens.pop(0)
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo + ou -'.format(tokens[0].nome, tokens[0].line))


def outros_termos(tokens):
    if tokens[0].tipo == '+' or tokens[0].tipo == '-':
        op_ad(tokens)
        termo(tokens)
        outros_termos(tokens)

def op_un(tokens):
    if tokens[0].tipo == '+' or tokens[0].tipo == '-':
        tokens.pop(0)


def expressao(tokens):
    termo(tokens)
    outros_termos(tokens)


def relacao(tokens):
    if tokens[0].tipo in ['=', ':=', '<', '>', '<=', '>=']:
        tokens.pop(0)
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo relação (=, <, >, >=, <=)'.format(tokens[0].nome, tokens[0].line))


def condicao(tokens):
    semantic.first_type = True
    expressao(tokens)
    relacao(tokens)
    expressao(tokens)

def comando(tokens):
    if tokens[0].tipo == 'read' or tokens[0].tipo == 'write':
        tokens.pop(0)
        if tokens[0].tipo == '(':
            tokens.pop(0)
            semantic.first_type = True
            variaveis(tokens)
            if tokens[0].tipo == ')':
                semantic.quee_insert = []
                tokens.pop(0)
            else:
                raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo )'.format(tokens[0].nome, tokens[0].line))
        else:
            raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo ('.format(tokens[0].nome, tokens[0].line))

    
    elif tokens[0].tipo == 'if':
        tokens.pop(0)
        condicao(tokens)
        if tokens[0].tipo == 'then':
            tokens.pop(0)
            comandos(tokens)
            pfalsa(tokens)
            if tokens[0].tipo == '$':
                tokens.pop(0)
            else:
                raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo $'.format(tokens[0].nome, tokens[0].line))
        else:
            raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo then'.format(tokens[0].nome, tokens[0].line))
    elif tokens[0].tipo == 'ident':
        semantic.search(tokens[0])
        semantic.first_type = True
        semantic.check_type(tokens[0])
        tokens.pop(0)
        if tokens[0].tipo == ':=':
            tokens.pop(0)
            expressao(tokens)
        else:
            raise SyntaxError('aaaaa')
        
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo read, write, if ou identifcador'.format(tokens[0].nome, tokens[0].line))


def mais_comandos(tokens):
    if tokens[0].tipo == ';':
        tokens.pop(0)
        comandos(tokens)


def comandos(tokens):
    comando(tokens)
    mais_comandos(tokens)


def pfalsa(tokens):
    if tokens[0].tipo == 'else':
        tokens.pop(0)
        comandos(tokens)

def mais_var(tokens):
    if tokens[0].tipo == ',':
        tokens.pop(0)
        variaveis(tokens)


def variaveis(tokens):
    if tokens[0].tipo == 'ident':
        semantic.append(tokens[0])
        tokens.pop(0)
        mais_var(tokens)
    else:
        raise SyntaxError(
            'O termo {} na linha {} é invalido. Falha no termo identificador'.format(tokens[0].nome,
                                                                                                     tokens[0].line))


def tipo_var(tokens):
    if tokens[0].tipo == 'real' or tokens[0].tipo == 'integer':
        semantic.insert(tokens[0].nome)
        tokens.pop(0)
    else:
        raise SyntaxError(
            'O termo {} na linha {} é invalido. Falha no termo real ou integer'.format(tokens[0].nome,
                                                                                                     tokens[0].line))


def dc_v(tokens):
    
    semantic.skip = True
    tipo_var(tokens)
    if tokens[0].tipo == ':':
        tokens.pop(0)
        variaveis(tokens)
        semantic.skip = False

def mais_dc(tokens):
    if tokens[0].tipo == ';':
        tokens.pop(0)
        dc(tokens)


def programa(tokens):
    if tokens[0].tipo == 'program':
        tokens.pop(0)
        if tokens[0].tipo == 'ident':
            semantic.append(tokens[0])
            semantic.insert('program')
            tokens.pop(0)
            corpo(tokens)
            if tokens[0].tipo == '.':
                tokens.pop(0)
            else:
                raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo .'.format(tokens[0].nome, tokens[0].line))
        else:
            raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo identificador'.format(tokens[0].nome, tokens[0].line))
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo program'.format(tokens[0].nome, tokens[0].line))


def corpo(tokens):
    dc(tokens)
    if tokens[0].tipo == 'begin':
        tokens.pop(0)
        comandos(tokens)
        if tokens[0].tipo == 'end':
            tokens.pop(0)
        else:
            raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo end'.format(tokens[0].nome, tokens[0].line))
    else:
        raise SyntaxError('O termo {} na linha {} é invalido. Falha no termo begin'.format(tokens[0].nome, tokens[0].line))


def dc(tokens):
   
    dc_v(tokens)
    mais_dc(tokens)
  



