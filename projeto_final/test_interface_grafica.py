"""Testes de widgets reais. Executar com display gráfico (ou Xvfb no Linux)."""
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from interface_grafica import AplicacaoBancaria
from persistencia import salvar_sessao
from sistema import SistemaBancario


class TesteInterface(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = AplicacaoBancaria(self.root)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(self.root.destroy)
        self.root.update()
        self.caminho = Path(self.tmp.name) / "sessao.json"

    def cadastrar(self, nome="Ana", prioridade="Normal"):
        self.app.nome.set(nome)
        self.app.prioridade.set(prioridade)
        self.app.cadastrar()
        self.root.update()

    def test_inicio_vazio_botoes_desabilitados(self):
        self.assertEqual(self.app.tabela_fila.get_children(), ())
        self.assertIn("disabled", self.app.botao_atender.state())
        self.assertIn("disabled", self.app.botao_desfazer.state())

    def test_cadastro_tabela_e_indicador(self):
        self.cadastrar()
        self.assertEqual(self.app.tabela_fila.get_children(), ("N001",))
        self.assertEqual(self.app.indicadores["pendentes"].get(), "1")
        self.assertEqual(self.app.nome.get(), "")
        self.assertTrue(self.app.alterado)

    def test_cadastro_invalido_mostra_erro(self):
        with patch("interface_grafica.messagebox.showerror") as erro:
            self.cadastrar(" ")
            erro.assert_called_once()
        self.assertEqual(self.app.sistema.pendentes(), 0)

    def test_prioritario_primeiro(self):
        self.cadastrar("Ana")
        self.cadastrar("Bia", "Prioritário")
        self.assertEqual(self.app.tabela_fila.get_children(), ("P001", "N001"))
        self.assertIn("P001", self.app.proximo_texto.get())

    def test_atender_desfazer_refazer_atualiza_historico(self):
        self.cadastrar()
        self.app.atender()
        self.assertEqual(len(self.app.tabela_historico.get_children()), 1)
        self.app.reverter(False)
        self.assertEqual(self.app.tabela_fila.get_children(), ("N001",))
        self.app.reverter(True)
        self.assertEqual(self.app.tabela_fila.get_children(), ())
        self.assertEqual(self.app.indicadores["atendidos"].get(), "1")

    def test_busca_nao_muda_ordem_atendimento(self):
        self.cadastrar("Ana")
        self.cadastrar("Bia", "Prioritário")
        self.app.busca.set("ana")
        self.root.update()
        self.assertEqual(self.app.tabela_fila.get_children(), ("N001",))
        self.app.atender()
        self.assertEqual(self.app.sistema.atendidos()[0].nome, "Bia")

    def test_reclassificacao_com_confirmacao(self):
        self.cadastrar()
        self.app.tabela_fila.selection_set("N001")
        with patch("interface_grafica.messagebox.askyesno", return_value=True):
            self.app.reclassificar()
        self.assertTrue(self.app.sistema.buscar_pendente("N001").prioritario)
        self.assertEqual(self.app.indicadores["prioritarios"].get(), "1")

    def test_cancelamento_recusado_preserva_fila(self):
        self.cadastrar()
        self.app.tabela_fila.selection_set("N001")
        with patch("interface_grafica.messagebox.askyesno", return_value=False):
            self.app.cancelar()
        self.assertEqual(self.app.sistema.pendentes(), 1)

    def test_cancelamento_confirmado(self):
        self.cadastrar()
        self.app.tabela_fila.selection_set("N001")
        with patch("interface_grafica.messagebox.askyesno", return_value=True):
            self.app.cancelar()
        self.assertEqual(self.app.indicadores["cancelados"].get(), "1")
        self.assertEqual(self.app.tabela_fila.get_children(), ())

    def test_salvar_e_abrir_sessao(self):
        self.cadastrar()
        with patch("interface_grafica.filedialog.asksaveasfilename", return_value=str(self.caminho)):
            self.assertTrue(self.app.salvar())
        self.assertFalse(self.app.alterado)
        self.app.sistema = SistemaBancario()
        with patch("interface_grafica.filedialog.askopenfilename", return_value=str(self.caminho)):
            self.app.abrir()
        self.assertEqual(self.app.sistema.pendentes(), 1)
        self.assertEqual(self.app.tabela_fila.get_children(), ("N001",))

    def test_abrir_corrompido_preserva_sessao(self):
        self.cadastrar()
        self.caminho.write_text("{erro")
        with patch("interface_grafica.filedialog.askopenfilename", return_value=str(self.caminho)), \
             patch("interface_grafica.messagebox.showerror") as erro:
            self.app.abrir()
            erro.assert_called_once()
        self.assertEqual(self.app.sistema.pendentes(), 1)

    def test_cancelar_dialogo_salvar_mantem_alterado(self):
        self.cadastrar()
        with patch("interface_grafica.filedialog.asksaveasfilename", return_value=""):
            self.assertFalse(self.app.salvar())
        self.assertTrue(self.app.alterado)

    def test_protecao_contra_perda_cancelar(self):
        self.cadastrar()
        with patch("interface_grafica.messagebox.askyesnocancel", return_value=None):
            self.assertFalse(self.app._confirmar_perda())

    def test_exportar_csv_nao_marca_sessao_salva(self):
        self.cadastrar()
        destino = self.caminho.with_suffix(".csv")
        with patch("interface_grafica.filedialog.asksaveasfilename", return_value=str(destino)):
            self.app.exportar()
        self.assertTrue(destino.exists())
        self.assertTrue(self.app.alterado)

    def test_abas_e_layout_minimo(self):
        self.root.geometry("1060x740")
        self.root.update()
        self.assertEqual(len(self.app.abas.tabs()), 3)
        self.assertTrue(self.app.botao_atender.winfo_viewable())
        self.assertTrue(self.app.botao_desfazer.winfo_viewable())
        self.assertTrue(self.app.botao_cancelar.winfo_viewable())
        self.assertGreaterEqual(self.app.botao_demo.winfo_height(), self.app.botao_demo.winfo_reqheight())
        self.assertLessEqual(self.app.botao_cancelar.winfo_rooty() + self.app.botao_cancelar.winfo_height(), self.root.winfo_height())
        self.assertLessEqual(self.app.botao_desfazer.winfo_rooty() + self.app.botao_desfazer.winfo_height(), self.root.winfo_height())
        self.assertLessEqual(self.app.botao_atender.winfo_rooty() + self.app.botao_atender.winfo_height(), self.root.winfo_height())
        self.app.abas.select(2)
        self.root.update()
        self.assertIn("DUAS PILHAS LIFO", self.app.estruturas_texto.get())
