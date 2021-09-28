import dataclasses

reservadas = ['real','integer','begin','read','if','then','write','else','end','program']

operadores = ["+","-","*","/","<",">","=","<=",">=",":=",";",":"]

delimitador = ['(',')','$', ',', '.']

@dataclasses.dataclass
class Token:
    nome: str
    tipo: str
    line: int
    
def seperar_palavras_juntas(lista_splitada):
    lista_retorno = []
    start = 0
    for palavra in lista_splitada:
        i =0
        start = 0
        tamanho = len(palavra)
        while i<tamanho:
            if (palavra[i] in delimitador) or (palavra[i] in operadores):
                if start < i:
                    lista_retorno.append(palavra[start: i])
                if (palavra[i]== '<' or palavra[i]== '>' or palavra[i]==':') and i<len(palavra):
                    if i+1< tamanho:
                        if palavra[i+1]== '=':
                            lista_retorno.append(palavra[i:i+2])
                            start = i+3
                            i += 3
                    else:
                        lista_retorno.append(palavra[i])
                        start = i+1
                        i += 1
                else:
                    lista_retorno.append(palavra[i])
                    start = i+1
                    i += 1


            else:
                i += 1
        if start < len(palavra):
                lista_retorno.append(palavra[start:])

    return lista_retorno


def detectar_reservadas(texto, lista_tokens):
        if texto in reservadas:
            lista_tokens.append(Token(texto, texto, 1))
            return True

def detectar_operadores(texto, lista_tokens):
    if texto in operadores:
        lista_tokens.append(Token(texto, texto, 1))
        return True

def detectar_delimitador(texto, lista_tokens):
    if texto in delimitador:
        lista_tokens.append(Token(texto, texto, 1))
        return True
def detectar_numero(texto, lista_tokens):
        try:

            a = int(texto)
            lista_tokens.append(Token(texto, 'integer'))
            return texto
        except:
            pass



def detectar_identificador(texto, lista_tokens):
    lista_tokens.append(Token(texto, 'ident', 1))


