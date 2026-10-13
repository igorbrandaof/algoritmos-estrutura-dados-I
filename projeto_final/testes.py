import unittest
from sistema import SistemaBancario
from estruturas import Fila,Pilha,ListaHistorico
class TesteEstruturas(unittest.TestCase):
 def test_fila(self):
  f=Fila();self.assertTrue(f.vazia());f.enfileirar(2);f.enfileirar(3);f.colocar_na_frente(1)
  self.assertEqual([f.desenfileirar() for _ in range(4)],[1,2,3,None])
 def test_pilha(self):
  p=Pilha();p.empilhar(1);p.empilhar(2);self.assertEqual(p.desempilhar(),2);self.assertEqual(p.topo(),1);p.limpar();self.assertTrue(p.vazia())
 def test_lista(self):
  l=ListaHistorico();l.inserir_inicio('a');l.inserir_inicio('b');self.assertEqual(tuple(l),('b','a'));self.assertEqual(l.remover_inicio(),'b')
class TesteSistema(unittest.TestCase):
 def test_prioridade_e_fifo(self):
  b=SistemaBancario();b.cadastrar('Ana');b.cadastrar('Bia',True);b.cadastrar('Caio',True);b.cadastrar('Davi')
  self.assertEqual([b.atender().nome for _ in range(4)],['Bia','Caio','Ana','Davi'])
  self.assertIsNone(b.atender())
 def test_senhas(self):
  b=SistemaBancario();self.assertEqual(b.cadastrar('A').senha,'N001');self.assertEqual(b.cadastrar('B',True).senha,'P001')
 def test_desfazer_sequencia(self):
  b=SistemaBancario();b.cadastrar('A');b.cadastrar('B');b.atender();b.atender()
  self.assertEqual(b.desfazer_ultimo().nome,'B');self.assertEqual(b.desfazer_ultimo().nome,'A')
  self.assertEqual([c.nome for c in b.filas()[1]],['A','B']);self.assertEqual(b.atendidos(),())
 def test_cadastro_invalida_desfazer(self):
  b=SistemaBancario();b.cadastrar('A');b.atender();b.cadastrar('B')
  self.assertIsNone(b.desfazer_ultimo());self.assertEqual(len(b.atendidos()),1)
 def test_busca(self):
  b=SistemaBancario();c=b.cadastrar('Ana');self.assertIsNone(b.consultar_atendimento(c.senha));b.atender();self.assertEqual(b.consultar_atendimento(c.senha),c)
 def test_vazio(self):
  b=SistemaBancario();self.assertIsNone(b.atender());self.assertIsNone(b.desfazer_ultimo())
 def test_nome_invalido(self):
  b=SistemaBancario()
  with self.assertRaises(ValueError):b.cadastrar('  ')
if __name__=='__main__':unittest.main()
