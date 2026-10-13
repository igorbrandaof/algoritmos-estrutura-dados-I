"""TAD Conta Bancaria com duas representacoes didaticas.
Estatico: vetor de capacidade fixa (lista Python prealocada).
Dinamico: nos ligados, alocados sob demanda pelo runtime Python.
Nao representa malloc/free; Python usa gerenciamento automatico.
"""
class Conta:
 def __init__(self,numero,titular,saldo=0):
  if not numero or not titular.strip() or saldo<0:raise ValueError('dados invalidos')
  self.numero=numero;self.titular=titular.strip();self._saldo=float(saldo)
 @property
 def saldo(self):return self._saldo
 def depositar(self,valor):
  if valor<=0:raise ValueError('valor deve ser positivo')
  self._saldo+=valor
 def sacar(self,valor):
  if valor<=0 or valor>self._saldo:raise ValueError('saldo insuficiente ou valor invalido')
  self._saldo-=valor

class BancoEstatico:
 def __init__(self,capacidade):
  if capacidade<1:raise ValueError('capacidade invalida')
  self._dados=[None]*capacidade;self._n=0
 def inserir(self,conta):
  if self.buscar(conta.numero) is not None:raise ValueError('numero duplicado')
  if self._n==len(self._dados):raise OverflowError('capacidade esgotada')
  self._dados[self._n]=conta;self._n+=1
 def buscar(self,numero):
  for i in range(self._n):
   if self._dados[i].numero==numero:return self._dados[i]
  return None
 def remover(self,numero):
  for i in range(self._n):
   if self._dados[i].numero==numero:
    conta=self._dados[i]
    for j in range(i,self._n-1):self._dados[j]=self._dados[j+1]
    self._n-=1;self._dados[self._n]=None
    return conta
  return None
 def quantidade(self):return self._n

class _No:
 def __init__(self,conta):self.conta=conta;self.proximo=None
class BancoDinamico:
 def __init__(self):self._inicio=None;self._n=0
 def inserir(self,conta):
  if self.buscar(conta.numero) is not None:raise ValueError('numero duplicado')
  novo=_No(conta);novo.proximo=self._inicio;self._inicio=novo;self._n+=1
 def buscar(self,numero):
  atual=self._inicio
  while atual:
   if atual.conta.numero==numero:return atual.conta
   atual=atual.proximo
  return None
 def remover(self,numero):
  anterior=None;atual=self._inicio
  while atual:
   if atual.conta.numero==numero:
    if anterior:anterior.proximo=atual.proximo
    else:self._inicio=atual.proximo
    self._n-=1;return atual.conta
   anterior,atual=atual,atual.proximo
  return None
 def quantidade(self):return self._n
