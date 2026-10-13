"""Regras: prioridade estrita; FIFO dentro de cada categoria.
Desfazer somente sequência de atendimentos desde o último cadastro.
Um novo cadastro invalida o histórico de desfazer, não o histórico de atendimento.
"""
from cliente import Cliente
from estruturas import Fila,Pilha,ListaHistorico
class SistemaBancario:
 def __init__(self):
  self.normal=Fila();self.prioritaria=Fila()
  self.historico=ListaHistorico();self.desfazer=Pilha()
  self._seq_normal=0;self._seq_prioritaria=0
 def cadastrar(self,nome,prioritario=False):
  if not isinstance(nome,str) or not nome.strip():raise ValueError('nome obrigatorio')
  if not isinstance(prioritario,bool):raise ValueError('prioridade deve ser booleana')
  if prioritario:
   self._seq_prioritaria+=1;senha=f'P{self._seq_prioritaria:03d}'
  else:
   self._seq_normal+=1;senha=f'N{self._seq_normal:03d}'
  cliente=Cliente(nome.strip(),senha,prioritario)
  (self.prioritaria if prioritario else self.normal).enfileirar(cliente)
  self.desfazer.limpar() # cadastro altera a fila: invalida reversões anteriores
  return cliente
 def atender(self):
  fila=self.prioritaria if not self.prioritaria.vazia() else self.normal
  cliente=fila.desenfileirar()
  if cliente is not None:
   self.historico.inserir_inicio(cliente)
   self.desfazer.empilhar(cliente)
  return cliente
 def desfazer_ultimo(self):
  cliente=self.desfazer.desempilhar()
  if cliente is None:return None
  removido=self.historico.remover_inicio()
  if removido!=cliente:raise RuntimeError('historico inconsistente')
  (self.prioritaria if cliente.prioritario else self.normal).colocar_na_frente(cliente)
  return cliente
 def filas(self):return tuple(self.prioritaria),tuple(self.normal)
 def atendidos(self):return tuple(self.historico)
 def consultar_atendimento(self,senha):return self.historico.buscar(senha)
 def pendentes(self):return self.prioritaria.quantidade+self.normal.quantidade
