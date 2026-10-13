import unittest
from contas import Conta,BancoEstatico,BancoDinamico
class Testes(unittest.TestCase):
 def test_implementacoes(self):
  for banco in (BancoEstatico(2),BancoDinamico()):
   c=Conta('1','Ana',50);banco.inserir(c);c.depositar(20);c.sacar(10)
   self.assertEqual(banco.buscar('1').saldo,60)
   self.assertEqual(banco.remover('1'),c)
   self.assertIsNone(banco.buscar('1'))
 def test_capacidade(self):
  b=BancoEstatico(1);b.inserir(Conta('1','Ana'))
  with self.assertRaises(OverflowError):b.inserir(Conta('2','Bia'))
 def test_saldo(self):
  c=Conta('1','Ana',10)
  with self.assertRaises(ValueError):c.sacar(11)
if __name__=='__main__':unittest.main()
