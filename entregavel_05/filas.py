class FilaCircular:
 def __init__(self,capacidade):
  if type(capacidade) is not int or capacidade<1:raise ValueError('capacidade invalida')
  self._v=[None]*capacidade;self._inicio=0;self._n=0
 def vazia(self):return self._n==0
 def enfileirar(self,v):
  if self._n==len(self._v):raise OverflowError('fila cheia')
  self._v[(self._inicio+self._n)%len(self._v)]=v;self._n+=1
 def desenfileirar(self):
  if self.vazia():return None
  v=self._v[self._inicio];self._v[self._inicio]=None
  self._inicio=(self._inicio+1)%len(self._v);self._n-=1;return v
 def frente(self):return None if self.vazia() else self._v[self._inicio]
 def tamanho(self):return self._n
class _No:
 def __init__(self,v):self.valor=v;self.proximo=None
class FilaEncadeada:
 def __init__(self):self._inicio=None;self._fim=None;self._n=0
 def vazia(self):return self._inicio is None
 def enfileirar(self,v):
  no=_No(v)
  if self._fim:self._fim.proximo=no
  else:self._inicio=no
  self._fim=no;self._n+=1
 def desenfileirar(self):
  if self.vazia():return None
  v=self._inicio.valor;self._inicio=self._inicio.proximo;self._n-=1
  if self._inicio is None:self._fim=None
  return v
 def frente(self):return None if self.vazia() else self._inicio.valor
 def tamanho(self):return self._n
class FilaPrioridade:
 """Prioridade estrita: prioritarios primeiro, FIFO em cada categoria."""
 def __init__(self):self._p=FilaEncadeada();self._n=FilaEncadeada()
 def enfileirar(self,cliente,prioritario=False):
  (self._p if prioritario else self._n).enfileirar(cliente)
 def desenfileirar(self):
  if not self._p.vazia():return self._p.desenfileirar()
  return self._n.desenfileirar()
 def vazia(self):return self._p.vazia() and self._n.vazia()
