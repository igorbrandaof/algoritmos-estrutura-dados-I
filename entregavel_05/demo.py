from filas import *
for tipo in (lambda:FilaCircular(3),FilaEncadeada):
 f=tipo();f.enfileirar('Ana');f.enfileirar('Bia');print(type(f).__name__,f.desenfileirar(),f.frente())
p=FilaPrioridade();p.enfileirar('Normal');p.enfileirar('Prioritario',True);print(p.desenfileirar(),p.desenfileirar())
