import unittest
from pilhas import *
class Testes(unittest.TestCase):
 def test_pilhas(self):
  for p in (PilhaArray(3),PilhaEncadeada()):
   self.assertTrue(p.vazia());p.push(1);p.push(2)
   self.assertEqual(p.topo(),2);self.assertEqual(p.pop(),2);self.assertEqual(p.pop(),1);self.assertIsNone(p.pop())
 def test_balanceamento(self):
  self.assertTrue(parenteses_balanceados('([{}])'))
  self.assertFalse(parenteses_balanceados('([)]'))
if __name__=='__main__':unittest.main()
