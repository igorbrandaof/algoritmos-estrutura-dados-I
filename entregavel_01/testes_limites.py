import unittest
from utilitarios import fatorial, fibonacci, busca_binaria, media, trocar_valores, incrementar_contador


class TestesLimites(unittest.TestCase):
    def test_recursao_bases(self):
        self.assertEqual([fatorial(i) for i in range(6)], [1, 1, 2, 6, 24, 120])
        self.assertEqual([fibonacci(i) for i in range(9)], [0, 1, 1, 2, 3, 5, 8, 13, 21])

    def test_tipos_invalidos(self):
        for funcao in (fatorial, fibonacci):
            for valor in (-1, 1.5, "2", None, True):
                with self.subTest(funcao=funcao.__name__, valor=valor), self.assertRaises(ValueError):
                    funcao(valor)

    def test_busca_vazia_extremidades_ausente(self):
        self.assertEqual(busca_binaria([], 1), -1)
        for alvo, esperado in ((1, 0), (9, 4), (4, -1), (10, -1)):
            self.assertEqual(busca_binaria([1, 3, 5, 7, 9], alvo), esperado)

    def test_busca_duplicatas(self):
        valores = [1, 2, 2, 2, 3]
        self.assertEqual(valores[busca_binaria(valores, 2)], 2)

    def test_media_vazia_e_negativos(self):
        with self.assertRaises(ValueError):
            media([])
        self.assertEqual(media([-2, 0, 2]), 0)

    def test_referencias_mutaveis_e_imutaveis(self):
        a, b = 1, 2
        self.assertEqual(trocar_valores(a, b), (2, 1))
        self.assertEqual((a, b), (1, 2))
        contador = {"valor": 0}
        alias = contador
        incrementar_contador(contador)
        self.assertEqual(alias["valor"], 1)
