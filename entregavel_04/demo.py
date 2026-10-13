from pilhas import *
for tipo in (lambda:PilhaArray(5),PilhaEncadeada):
 p=tipo();p.push(10);p.push(20);print(type(p).__name__,p.topo(),p.pop(),p.pop())
for x in ('(a+[b])','([)]'):print(x,parenteses_balanceados(x))
