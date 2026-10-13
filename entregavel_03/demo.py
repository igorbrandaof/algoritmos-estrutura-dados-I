from listas import ListaSequencial,ListaSimples,ListaDupla,ListaCircular
for classe in (lambda:ListaSequencial(5),ListaSimples):
 lista=classe();lista.inserir(0,'Ana');lista.inserir(1,'Bia');print(type(lista).__name__,lista.percorrer(),lista.buscar('Bia'));lista.remover(0)
dupla=ListaDupla();dupla.inserir_fim(1);dupla.inserir_fim(2);print('Dupla',dupla.percorrer(),dupla.reverso())
circular=ListaCircular();circular.inserir_fim(3);circular.inserir_fim(4);print('Circular',circular.percorrer())
