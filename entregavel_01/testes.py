import unittest
from utilitarios import *
class TesteUtilitarios(unittest.TestCase):
 def test_fatorial(self): self.assertEqual(fatorial(5),120)
 def test_fibonacci(self): self.assertEqual(fibonacci(7),13)
 def test_busca(self): self.assertEqual(busca_binaria([1,3,5,7],5),2);self.assertEqual(busca_binaria([1,3],4),-1)
 def test_troca(self): self.assertEqual(trocar_valores(2,3),(3,2))
 def test_mutacao(self):
  d={'valor':1};incrementar_contador(d);self.assertEqual(d['valor'],2)
 def test_media(self): self.assertEqual(media([2,4,6]),4)
 def test_invalido(self):
  with self.assertRaises(ValueError):fatorial(-1)
if __name__=='__main__':unittest.main()
