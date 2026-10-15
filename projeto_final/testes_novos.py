"""Regressões do fluxo, invariantes de fila e fronteira de persistência."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sistema import SistemaBancario
from persistencia import carregar_sessao, salvar_sessao, exportar_csv


class TesteOperacoes(unittest.TestCase):
    def setUp(self):
        self.b = SistemaBancario()
        self.a = self.b.cadastrar("Ana")
        self.p = self.b.cadastrar("Bia", True)
        self.c = self.b.cadastrar("Caio")

    def test_prioridade_consistente_com_proximo(self):
        self.assertEqual(self.b.proximo(), self.p)
        self.assertEqual(self.b.atender(), self.p)
        self.assertEqual(self.b.proximo(), self.a)

    def test_refazer_atendimento(self):
        self.b.atender()
        self.b.desfazer_ultimo()
        self.assertEqual(self.b.proximo(), self.p)
        self.assertEqual(self.b.refazer_ultimo(), self.p)
        self.assertEqual(self.b.atendidos(), (self.p,))

    def test_reclassificar_preserva_chegada_e_senha(self):
        novo = self.b.reclassificar(self.a.senha, True)
        self.assertEqual(novo.senha, self.a.senha)
        self.assertEqual(self.b.proximo(), novo)
        self.assertEqual([c.nome for c in self.b.fila_ordenada()], ["Ana", "Bia", "Caio"])

    def test_reclassificar_desfazer_refazer(self):
        novo = self.b.reclassificar(self.a.senha, True)
        self.assertEqual(self.b.desfazer_ultimo(), self.a)
        self.assertEqual(self.b.proximo(), self.p)
        self.assertEqual(self.b.refazer_ultimo(), novo)
        self.assertEqual(self.b.proximo(), novo)

    def test_operacoes_intercaladas(self):
        novo = self.b.reclassificar(self.a.senha, True)
        self.b.atender()
        self.assertEqual(self.b.desfazer_ultimo(), novo)
        self.assertEqual(self.b.desfazer_ultimo(), self.a)
        self.b.refazer_ultimo()
        self.b.refazer_ultimo()
        self.assertEqual(self.b.atendidos(), (novo,))
        self.assertEqual(self.b.proximo(), self.p)

    def test_nova_operacao_invalida_refazer(self):
        self.b.atender()
        self.b.desfazer_ultimo()
        self.b.reclassificar(self.c.senha, True)
        self.assertIsNone(self.b.refazer_ultimo())

    def test_cadastro_invalida_ambas_pilhas(self):
        self.b.atender()
        self.b.desfazer_ultimo()
        self.b.cadastrar("Davi")
        self.assertIsNone(self.b.desfazer_ultimo())
        self.assertIsNone(self.b.refazer_ultimo())

    def test_cancelar_limpa_reversoes_e_mantem_historico(self):
        self.b.atender()
        self.assertEqual(self.b.cancelar(self.a.senha), self.a)
        self.assertEqual(self.b.atendidos(), (self.p,))
        self.assertIsNone(self.b.desfazer_ultimo())
        self.assertEqual(self.b.estatisticas()["cancelados"], 1)

    def test_cancelar_inexistente_nao_muda_pilhas(self):
        self.b.atender()
        self.assertIsNone(self.b.cancelar("N999"))
        self.assertEqual(self.b.desfazer_ultimo(), self.p)

    def test_reclassificar_categoria_igual_nao_invalida_pilhas(self):
        self.b.atender()
        self.b.desfazer_ultimo()
        self.b.reclassificar(self.a.senha, False)
        self.assertEqual(self.b.refazer_ultimo(), self.p)

    def test_reclassificar_atendido_rejeita(self):
        self.b.atender()
        with self.assertRaises(ValueError):
            self.b.reclassificar(self.p.senha, False)

    def test_categoria_invalida_rejeita(self):
        with self.assertRaises(ValueError):
            self.b.reclassificar(self.a.senha, "sim")

    def test_pesquisa_nome_senha_sem_sensibilidade_caixa(self):
        self.assertEqual(self.b.pesquisar("ANA"), (self.a,))
        self.assertEqual(self.b.pesquisar("n001"), (self.a,))
        self.b.atender()
        self.assertEqual(self.b.pesquisar("bia", historico=True), (self.p,))

    def test_normalizar_nome(self):
        self.assertEqual(self.b.cadastrar("  Eva   Lima  ").nome, "Eva Lima")

    def test_nome_longo_nao_consume_senha(self):
        with self.assertRaises(ValueError):
            self.b.cadastrar("a" * 101)
        self.assertEqual(self.b.cadastrar("Davi").senha, "N003")

    def test_estatisticas_totais(self):
        self.b.atender()
        self.b.cancelar(self.c.senha)
        e = self.b.estatisticas()
        self.assertEqual(e["cadastrados"], e["pendentes"] + e["atendidos"] + e["cancelados"])

    def test_remover_fim_e_inserir_novamente(self):
        self.b.cancelar(self.c.senha)
        d = self.b.cadastrar("Davi")
        self.assertEqual(tuple(self.b.normal), (self.a, d))
        self.assertEqual(self.b.normal.fim.valor, d)

    def test_esvaziar_e_reutilizar_fila(self):
        self.b.cancelar(self.a.senha)
        self.b.cancelar(self.c.senha)
        self.assertIsNone(self.b.normal.fim)
        self.assertIsNone(self.b.normal.inicio)
        self.b.cadastrar("Davi")
        self.assertEqual(self.b.normal.quantidade, 1)

    def test_fluxo_longo_desfazer_refazer(self):
        b = SistemaBancario()
        clientes = [b.cadastrar(f"Cliente {i}", i % 3 == 0) for i in range(80)]
        ordem = b.fila_ordenada()
        for c in ordem:
            self.assertEqual(b.atender(), c)
        for _ in clientes:
            b.desfazer_ultimo()
        self.assertEqual(b.fila_ordenada(), ordem)
        for c in ordem:
            self.assertEqual(b.refazer_ultimo(), c)
        self.assertEqual(b.pendentes(), 0)


class TestePersistencia(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "sessao.json"
        self.b = SistemaBancario()
        self.a = self.b.cadastrar("Ana")
        self.p = self.b.cadastrar("João", True)
        self.b.cadastrar("Caio")
        self.b.atender()
        salvar_sessao(self.b, self.path)

    def _adulterar(self, mudar):
        d = json.loads(self.path.read_text())
        mudar(d)
        self.path.write_text(json.dumps(d))
        with self.assertRaises(ValueError):
            carregar_sessao(self.path)

    def test_roundtrip_e_contadores(self):
        novo = carregar_sessao(self.path)
        self.assertEqual(novo.fila_ordenada(), self.b.fila_ordenada())
        self.assertEqual(novo.atendidos(), self.b.atendidos())
        self.assertEqual(novo.cadastrar("Davi").senha, "N003")
        self.assertIsNone(novo.desfazer_ultimo())

    def test_roundtrip_reclassificacao_cancelamento(self):
        self.b.reclassificar(self.a.senha, True)
        self.b.cancelar("N002")
        salvar_sessao(self.b, self.path)
        novo = carregar_sessao(self.path)
        self.assertEqual(novo.fila_ordenada(), self.b.fila_ordenada())
        self.assertEqual(novo.estatisticas(), self.b.estatisticas())

    def test_json_corrompido(self):
        self.path.write_text("{erro")
        with self.assertRaises(ValueError):
            carregar_sessao(self.path)

    def test_versao_invalida(self):
        self._adulterar(lambda d: d.update(versao=999))

    def test_cliente_duplicado(self):
        self._adulterar(lambda d: d["normal"].append(d["normal"][0]))

    def test_fila_incorreta(self):
        self._adulterar(lambda d: d["normal"][0].update(prioritario=True))

    def test_prioridade_string(self):
        self._adulterar(lambda d: d["normal"][0].update(prioritario="false"))

    def test_contador_booleano(self):
        self._adulterar(lambda d: d["contadores"].update(ordem=True))

    def test_totais_inconsistentes(self):
        self._adulterar(lambda d: d["contadores"].update(cancelados=2))

    def test_ordem_fifo_invertida(self):
        self._adulterar(lambda d: d["normal"].reverse())

    def test_senha_invalida(self):
        self._adulterar(lambda d: d["normal"][0].update(senha="N000"))

    def test_ordem_duplicada(self):
        self._adulterar(lambda d: d["normal"][1].update(ordem=d["normal"][0]["ordem"]))

    def test_limite_tamanho(self):
        with patch("persistencia.LIMITE_ARQUIVO", 1):
            with self.assertRaises(ValueError):
                carregar_sessao(self.path)

    def test_salvamento_atomico_em_falha(self):
        anterior = self.path.read_bytes()
        with patch("persistencia.os.replace", side_effect=OSError("falha simulada")):
            with self.assertRaises(OSError):
                salvar_sessao(self.b, self.path)
        self.assertEqual(self.path.read_bytes(), anterior)
        self.assertEqual(list(self.path.parent.glob(".sessao-*")), [])

    def test_csv_nome_com_delimitador_e_unicode(self):
        c = self.b.cadastrar("José; Silva")
        csv_path = self.path.with_suffix(".csv")
        exportar_csv(self.b, csv_path)
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            linhas = list(csv.reader(f, delimiter=";"))
        self.assertTrue(any(linha[1:3] == [c.senha, c.nome] for linha in linhas))
        self.assertEqual(len(linhas), 5)

    def test_csv_formula_nao_e_executavel(self):
        self.b.cadastrar("=1+1")
        csv_path = self.path.with_suffix(".csv")
        exportar_csv(self.b, csv_path)
        self.assertIn("'=1+1", csv_path.read_text(encoding="utf-8-sig"))

    def test_sessao_vazia(self):
        salvar_sessao(SistemaBancario(), self.path)
        self.assertEqual(carregar_sessao(self.path).pendentes(), 0)
