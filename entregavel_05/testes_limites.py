import unittest
from filas import FilaCircular, FilaEncadeada, FilaPrioridade


class TestesLimites(unittest.TestCase):
    def test_fifo_ambas_representacoes(self):
        for fila in (FilaCircular(3), FilaEncadeada()):
            for i in range(3):
                fila.enfileirar(i)
            self.assertEqual(fila.frente(), 0)
            self.assertEqual([fila.desenfileirar() for _ in range(4)], [0, 1, 2, None])
            self.assertTrue(fila.vazia())
            fila.enfileirar(9)
            self.assertEqual(fila.frente(), 9)

    def test_circular_varias_voltas(self):
        f = FilaCircular(2)
        for i in range(30):
            f.enfileirar(i)
            self.assertEqual(f.desenfileirar(), i)
        self.assertEqual(f.tamanho(), 0)

    def test_overflow_nao_perde_elementos(self):
        f = FilaCircular(1)
        f.enfileirar("a")
        with self.assertRaises(OverflowError):
            f.enfileirar("b")
        self.assertEqual(f.desenfileirar(), "a")

    def test_prioridade_e_fifo_em_cada_categoria(self):
        f = FilaPrioridade()
        for c, p in (("N1", False), ("P1", True), ("N2", False), ("P2", True)):
            f.enfileirar(c, p)
        self.assertEqual([f.desenfileirar() for _ in range(5)], ["P1", "P2", "N1", "N2", None])

    def test_capacidade_invalida(self):
        for n in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                FilaCircular(n)
