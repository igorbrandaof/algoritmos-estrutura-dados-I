import unittest
from decimal import Decimal
from contas import Conta, BancoEstatico, BancoDinamico


class TestesLimites(unittest.TestCase):
    def test_centavos_exatos(self):
        c = Conta("1", "Ana")
        c.depositar("0.10")
        c.depositar("0.20")
        self.assertEqual(c.saldo, Decimal("0.30"))
        c.sacar("0.30")
        self.assertEqual(c.saldo, 0)

    def test_valores_invalidos_nao_alteram_saldo(self):
        for valor in (0, -1, float("nan"), float("inf"), True, "erro", "0.001", "1e100"):
            c = Conta("1", "Ana", 10)
            for operacao in (c.depositar, c.sacar):
                with self.subTest(valor=valor), self.assertRaises(ValueError):
                    operacao(valor)
                self.assertEqual(c.saldo, 10)

    def test_dados_invalidos(self):
        for dados in (("", "Ana", 0), ("1", " ", 0), ("1", "Ana", -1), (None, "Ana", 0)):
            with self.assertRaises(ValueError):
                Conta(*dados)

    def test_capacidade_invalida(self):
        for valor in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                BancoEstatico(valor)

    def test_duplicata_em_ambos_tads(self):
        for banco in (BancoEstatico(3), BancoDinamico()):
            banco.inserir(Conta("1", "Ana"))
            with self.assertRaises(ValueError):
                banco.inserir(Conta("1", "Bia"))
            self.assertEqual(banco.quantidade(), 1)

    def test_remover_inicio_meio_fim_e_reutilizar(self):
        for banco in (BancoEstatico(3), BancoDinamico()):
            for i in range(3):
                banco.inserir(Conta(str(i), f"Cliente {i}"))
            for i in (1, 0, 2):
                self.assertEqual(banco.remover(str(i)).numero, str(i))
            self.assertIsNone(banco.remover("ausente"))
            banco.inserir(Conta("novo", "Davi"))
            self.assertEqual(banco.quantidade(), 1)
