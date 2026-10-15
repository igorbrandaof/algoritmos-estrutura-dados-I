import unittest
from pilhas import PilhaArray, PilhaEncadeada, parenteses_balanceados


class TestesLimites(unittest.TestCase):
    def test_lifo_ambas_representacoes(self):
        for p in (PilhaArray(3), PilhaEncadeada()):
            for i in range(3):
                p.push(i)
            self.assertEqual(p.topo(), 2)
            self.assertEqual([p.pop() for _ in range(4)], [2, 1, 0, None])
            self.assertIsNone(p.topo())

    def test_overflow_e_reutilizacao(self):
        p = PilhaArray(1)
        p.push(1)
        with self.assertRaises(OverflowError):
            p.push(2)
        self.assertEqual(p.pop(), 1)
        p.push(3)
        self.assertEqual(p.topo(), 3)

    def test_balanceados_com_texto(self):
        for texto in ("", "abc", "([{}])", "f(x[0]) + {1}"):
            self.assertTrue(parenteses_balanceados(texto))

    def test_balanceamento_falhas(self):
        for texto in (")", "(", "([)]", "(()", "{]", "[]]"):
            self.assertFalse(parenteses_balanceados(texto))

    def test_capacidade_invalida(self):
        for n in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                PilhaArray(n)
