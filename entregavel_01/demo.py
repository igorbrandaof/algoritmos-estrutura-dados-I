from utilitarios import *
if __name__=='__main__':
    print('Fatorial(5):',fatorial(5))
    print('Fibonacci(7):',fibonacci(7))
    print('Busca binaria:',busca_binaria([1,3,5,7],5))
    print('Troca:',trocar_valores(4,9))
    contador={'valor':0};incrementar_contador(contador);print('Mutacao:',contador)
