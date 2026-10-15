import unittest
from listas import ListaSequencial, ListaSimples, ListaDupla, ListaCircular


class TestesLimites(unittest.TestCase):
    def test_limites_de_indice(self):
        for lista in (ListaSequencial(3), ListaSimples()):
            for indice in (-1, 1):
                with self.assertRaises(IndexError):
                    lista.inserir(indice, "a")
            with self.assertRaises(IndexError):
                lista.remover(0)
            lista.inserir(0, "a")
            with self.assertRaises(IndexError):
                lista.remover(1)
            self.assertEqual(lista.percorrer(), ["a"])

    def test_insercao_remocao_meio(self):
        for lista in (ListaSequencial(3), ListaSimples()):
            lista.inserir(0, 1)
            lista.inserir(1, 3)
            lista.inserir(1, 2)
            self.assertEqual(lista.percorrer(), [1, 2, 3])
            self.assertEqual(lista.remover(1), 2)
            self.assertEqual(lista.percorrer(), [1, 3])

    def test_capacidade_e_reaproveitamento(self):
        l = ListaSequencial(1)
        l.inserir(0, "a")
        with self.assertRaises(OverflowError):
            l.inserir(1, "b")
        l.remover(0)
        l.inserir(0, "b")
        self.assertEqual(l.percorrer(), ["b"])

    def test_dupla_referencias_apos_esvaziar(self):
        l = ListaDupla()
        self.assertIsNone(l.remover_fim())
        l.inserir_fim(1)
        l.inserir_fim(2)
        self.assertEqual(l.reverso(), [2, 1])
        l.remover_fim()
        l.remover_fim()
        self.assertIsNone(l.inicio)
        self.assertIsNone(l.fim)
        l.inserir_fim(3)
        self.assertIsNone(l.fim.anterior)

    def test_circular_ciclo_e_reutilizacao(self):
        l = ListaCircular()
        l.inserir_fim(1)
        self.assertIs(l.fim.proximo, l.fim)
        l.inserir_fim(2)
        self.assertEqual(l.percorrer(), [1, 2])
        self.assertEqual(l.remover_inicio(), 1)
        self.assertEqual(l.remover_inicio(), 2)
        self.assertIsNone(l.fim)
        l.inserir_fim(3)
        self.assertEqual(l.percorrer(), [3])

    def test_busca_ausente(self):
        for lista in (ListaSequencial(2), ListaSimples(), ListaDupla(), ListaCircular()):
            self.assertEqual(lista.buscar(999), -1)
