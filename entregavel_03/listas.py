"""TADs: lista sequencial fixa, simplesmente encadeada, dupla e circular."""
class ListaSequencial:
 def __init__(self,capacidade):
  if capacidade<=0:raise ValueError('capacidade invalida')
  self._v=[None]*capacidade;self._n=0
 def inserir(self,indice,valor):
  if not 0<=indice<=self._n:raise IndexError(indice)
  if self._n==len(self._v):raise OverflowError('lista cheia')
  for i in range(self._n,indice,-1):self._v[i]=self._v[i-1]
  self._v[indice]=valor;self._n+=1
 def remover(self,indice):
  if not 0<=indice<self._n:raise IndexError(indice)
  v=self._v[indice]
  for i in range(indice,self._n-1):self._v[i]=self._v[i+1]
  self._n-=1;self._v[self._n]=None;return v
 def buscar(self,valor):
  for i in range(self._n):
   if self._v[i]==valor:return i
  return -1
 def percorrer(self):return self._v[:self._n]

class _No:
 def __init__(self,valor):self.valor=valor;self.proximo=None
class ListaSimples:
 def __init__(self):self.inicio=None
 def inserir(self,indice,valor):
  if indice<0:raise IndexError(indice)
  novo=_No(valor)
  if indice==0:novo.proximo=self.inicio;self.inicio=novo;return
  anterior=self.inicio
  for _ in range(indice-1):
   if anterior is None:raise IndexError(indice)
   anterior=anterior.proximo
  if anterior is None:raise IndexError(indice)
  novo.proximo=anterior.proximo;anterior.proximo=novo
 def remover(self,indice):
  if indice<0 or self.inicio is None:raise IndexError(indice)
  if indice==0:v=self.inicio.valor;self.inicio=self.inicio.proximo;return v
  anterior=self.inicio
  for _ in range(indice-1):
   if anterior is None:raise IndexError(indice)
   anterior=anterior.proximo
  if anterior is None or anterior.proximo is None:raise IndexError(indice)
  v=anterior.proximo.valor;anterior.proximo=anterior.proximo.proximo;return v
 def buscar(self,valor):
  atual=self.inicio;i=0
  while atual:
   if atual.valor==valor:return i
   atual=atual.proximo;i+=1
  return -1
 def percorrer(self):
  res=[];atual=self.inicio
  while atual:res.append(atual.valor);atual=atual.proximo
  return res

class _NoDuplo:
 def __init__(self,valor):self.valor=valor;self.anterior=None;self.proximo=None
class ListaDupla:
 def __init__(self):self.inicio=None;self.fim=None
 def inserir_fim(self,valor):
  no=_NoDuplo(valor);no.anterior=self.fim
  if self.fim:self.fim.proximo=no
  else:self.inicio=no
  self.fim=no
 def remover_fim(self):
  if not self.fim:return None
  valor=self.fim.valor;self.fim=self.fim.anterior
  if self.fim:self.fim.proximo=None
  else:self.inicio=None
  return valor
 def buscar(self,valor):
  for i,x in enumerate(self.percorrer()):
   if x==valor:return i
  return -1
 def percorrer(self):
  out=[];no=self.inicio
  while no:out.append(no.valor);no=no.proximo
  return out
 def reverso(self):
  out=[];no=self.fim
  while no:out.append(no.valor);no=no.anterior
  return out

class ListaCircular:
 def __init__(self):self.fim=None
 def inserir_fim(self,valor):
  no=_No(valor)
  if self.fim is None:no.proximo=no
  else:no.proximo=self.fim.proximo;self.fim.proximo=no
  self.fim=no
 def remover_inicio(self):
  if self.fim is None:return None
  inicio=self.fim.proximo;valor=inicio.valor
  if inicio is self.fim:self.fim=None
  else:self.fim.proximo=inicio.proximo
  return valor
 def buscar(self,valor):
  for i,x in enumerate(self.percorrer()):
   if x==valor:return i
  return -1
 def percorrer(self):
  if self.fim is None:return []
  out=[];no=self.fim.proximo
  while True:
   out.append(no.valor);no=no.proximo
   if no is self.fim.proximo:break
  return out
