class PilhaArray:
 def __init__(self,capacidade):
  if type(capacidade) is not int or capacidade<1:raise ValueError('capacidade invalida')
  self._dados=[None]*capacidade;self._n=0
 def vazia(self):return self._n==0
 def push(self,v):
  if self._n==len(self._dados):raise OverflowError('pilha cheia')
  self._dados[self._n]=v;self._n+=1
 def pop(self):
  if self.vazia():return None
  self._n-=1;v=self._dados[self._n];self._dados[self._n]=None;return v
 def topo(self):return None if self.vazia() else self._dados[self._n-1]
class _No:
 def __init__(self,v,proximo=None):self.valor=v;self.proximo=proximo
class PilhaEncadeada:
 def __init__(self):self._topo=None
 def vazia(self):return self._topo is None
 def push(self,v):self._topo=_No(v,self._topo)
 def pop(self):
  if self.vazia():return None
  v=self._topo.valor;self._topo=self._topo.proximo;return v
 def topo(self):return None if self.vazia() else self._topo.valor

def parenteses_balanceados(texto):
 pilha=PilhaEncadeada();pares={')':'(',']':'[','}':'{'}
 for c in texto:
  if c in '([{':pilha.push(c)
  elif c in pares:
   if pilha.pop()!=pares[c]:return False
 return pilha.vazia()
