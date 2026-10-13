"""Biblioteca de funções matemáticas e utilitárias: módulo 1."""
def fatorial(n):
    if not isinstance(n,int) or n<0: raise ValueError('n deve ser inteiro nao negativo')
    if n<=1:return 1
    return n*fatorial(n-1)

def fibonacci(n):
    if not isinstance(n,int) or n<0: raise ValueError('n deve ser inteiro nao negativo')
    if n<=1:return n
    return fibonacci(n-1)+fibonacci(n-2)

def busca_binaria(valores, alvo, inicio=0, fim=None):
    """Recebe sequência ordenada crescente; retorna índice ou -1."""
    if fim is None: fim=len(valores)-1
    if inicio>fim:return -1
    meio=(inicio+fim)//2
    if valores[meio]==alvo:return meio
    if alvo<valores[meio]:return busca_binaria(valores,alvo,inicio,meio-1)
    return busca_binaria(valores,alvo,meio+1,fim)

def trocar_valores(a,b):
    """Imutáveis: retorna novos valores; argumentos originais não mudam."""
    return b,a

def incrementar_contador(contador):
    """Objeto mutável: altera o dicionário recebido por referência de objeto."""
    contador['valor']+=1
    return contador['valor']

def media(valores):
    if not valores: raise ValueError('sequencia vazia')
    return sum(valores)/len(valores)
