from analisador_sintatico import programa
from lexico import * 
with open('./correto.lalg.txt', "r") as t:
    texto = t.read().split()
texto2 = seperar_palavras_juntas(texto)
lista_tokens = []
print(texto2)
for palavra in texto2:
    flag = detectar_reservadas(palavra, lista_tokens)
    if not flag:
        flag = detectar_operadores(palavra, lista_tokens)
        if not flag:
            flag = detectar_delimitador(palavra, lista_tokens)
            if not flag:
               flag = detectar_identificador(palavra, lista_tokens)
               if not flag:
                    detectar_numero(palavra, lista_tokens)

print(lista_tokens)

programa(lista_tokens)
