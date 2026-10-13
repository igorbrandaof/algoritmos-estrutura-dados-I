import unittest
from filas import *
class Testes(unittest.TestCase):
 def test_filas(self):
  for f in (FilaCircular(3),FilaEncadeada()):
   f.enfileirar('A');f.enfileirar('B');self.assertEqual(f.desenfileirar(),'A');self.assertEqual(f.frente(),'B')
   f.enfileirar('C');self.assertEqual(f.desenfileirar(),'B');self.assertEqual(f.desenfileirar(),'C');self.assertTrue(f.vazia())
 def test_circular_wrap(self):
  f=FilaCircular(2);f.enfileirar(1);f.enfileirar(2);f.desenfileirar();f.enfileirar(3);self.assertEqual([f.desenfileirar(),f.desenfileirar()],[2,3])
 def test_prioridade(self):
  f=FilaPrioridade();f.enfileirar('N1');f.enfileirar('P1',True);f.enfileirar('P2',True)
  self.assertEqual([f.desenfileirar() for _ in range(3)],['P1','P2','N1'])
if __name__=='__main__':unittest.main()
