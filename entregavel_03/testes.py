import unittest
from listas import *
class Testes(unittest.TestCase):
 def test_listas(self):
  for x in (ListaSequencial(5),ListaSimples()):
   x.inserir(0,'A');x.inserir(1,'C');x.inserir(1,'B')
   self.assertEqual(x.percorrer(),['A','B','C'])
   self.assertEqual(x.buscar('B'),1)
   self.assertEqual(x.remover(1),'B')
 def test_dupla(self):
  x=ListaDupla();x.inserir_fim(1);x.inserir_fim(2)
  self.assertEqual(x.reverso(),[2,1]);self.assertEqual(x.remover_fim(),2)
 def test_circular(self):
  x=ListaCircular();x.inserir_fim(1);x.inserir_fim(2)
  self.assertEqual(x.percorrer(),[1,2]);self.assertEqual(x.remover_inicio(),1)
if __name__=='__main__':unittest.main()
