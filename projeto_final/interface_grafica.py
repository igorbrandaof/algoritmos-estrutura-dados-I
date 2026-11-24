"""Interface desktop em Tkinter/ttk; todas as regras vivem em SistemaBancario."""
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from tkinter import font as tkfont

if __package__:
    from .sistema import SistemaBancario
    from .persistencia import carregar_sessao, salvar_sessao, exportar_csv
else:
    from sistema import SistemaBancario
    from persistencia import carregar_sessao, salvar_sessao, exportar_csv

FUNDO = "#f3f5f9"
AZUL = "#152b4a"
VERDE = "#087f70"
TEXTO = "#24354b"
CINZA = "#63748b"


def preencher_demonstracao(sistema):
    """Dados fictícios, carregados apenas por ação explícita ou --demo."""
    for nome, prioridade in (("Ana Oliveira", False), ("Carlos Mendes", True),
                             ("Marina Costa", False), ("João Santos", True),
                             ("Beatriz Lima", False), ("Lucas Ferreira", False)):
        sistema.cadastrar(nome, prioridade)
    sistema.atender()


class AplicacaoBancaria:
    def __init__(self, root, sistema=None):
        self.root = root
        self.sistema = sistema if sistema is not None else SistemaBancario()
        self.alterado = False
        self.caminho = None
        self.nome = tk.StringVar()
        self.prioridade = tk.StringVar(value="Normal")
        self.busca = tk.StringVar()
        self.status = tk.StringVar(value="Pronto. Cadastre um cliente para iniciar o atendimento.")
        self.root.title("Central de Atendimento Bancário")
        self.root.geometry("1000x700")
        self.root.minsize(900, 640)
        self.root.configure(bg=FUNDO)
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self._estilos()
        self._construir()
        self.busca.trace_add("write", lambda *_: self.atualizar())
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        self.root.bind("<Control-s>", lambda _: self.salvar())
        self.root.bind("<Control-z>", lambda _: self.reverter(False))
        self.root.bind("<Control-y>", lambda _: self.reverter(True))
        self.atualizar()
        self.entrada_nome.focus_set()

    def _estilos(self):
        familias = {f.casefold(): f for f in tkfont.families(self.root)}
        self.fonte = next((familias[f.casefold()] for f in ("Segoe UI", "DejaVu Sans", "Helvetica", "Arial") if f.casefold() in familias), "TkDefaultFont")
        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=FUNDO)
        estilo.configure("TLabel", background=FUNDO, foreground=TEXTO, font=(self.fonte, 10))
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("Card.TLabel", background="white", foreground=TEXTO)
        estilo.configure("Muted.TLabel", background="white", foreground=CINZA, font=(self.fonte, 9))
        estilo.configure("TLabelframe", background="white", bordercolor="#d5dbe2", relief="solid")
        estilo.configure("TLabelframe.Label", background="white", foreground=TEXTO, font=(self.fonte, 10, "bold"))
        estilo.configure("TButton", font=(self.fonte, 10), padding=(12, 8), background="white", foreground=TEXTO)
        estilo.map("TButton", background=[("active", "#e8edf3")], foreground=[("disabled", "#969da8")])
        estilo.configure("Primary.TButton", background=AZUL, foreground="white", borderwidth=0)
        estilo.map("Primary.TButton", background=[("disabled", "#c3ccd6"), ("active", "#23486e")],
                   foreground=[("disabled", "#65778a")])
        estilo.configure("TEntry", padding=7, fieldbackground="white")
        estilo.configure("TCombobox", padding=7, fieldbackground="white")
        estilo.configure("Treeview", background="white", fieldbackground="white", foreground=TEXTO,
                         rowheight=34, font=(self.fonte, 10), borderwidth=0)
        estilo.configure("Treeview.Heading", background="#edf1f5", foreground=TEXTO,
                         padding=(10, 9), font=(self.fonte, 9, "bold"), relief="flat")
        estilo.map("Treeview", background=[("selected", "#dbe8f5")], foreground=[("selected", TEXTO)])
        estilo.configure("TNotebook", background=FUNDO, borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(18, 9), font=(self.fonte, 10))
        estilo.map("TNotebook.Tab", background=[("selected", "white")])

    def _construir(self):
        self.menu_arquivo = tk.Menu(self.root, tearoff=False)
        for titulo, comando in (("Abrir sessão...", self.abrir), ("Salvar sessão...", self.salvar),
                                ("Exportar CSV...", self.exportar)):
            self.menu_arquivo.add_command(label=titulo, command=comando)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label="Carregar demonstração", command=self.demonstracao)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label="Sair", command=self.fechar)
        menu = tk.Menu(self.root)
        menu.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.root.configure(menu=menu)

        cabecalho = ttk.Frame(self.root, padding=(22, 18, 22, 12))
        cabecalho.grid(row=0, column=0, sticky="ew")
        ttk.Label(cabecalho, text="Central de Atendimento Bancário",
                  font=(self.fonte, 20, "bold")).pack(anchor="w")
        ttk.Label(cabecalho, text="Controle de senhas e fila de atendimento", foreground=CINZA).pack(anchor="w", pady=(4, 0))

        cadastro = ttk.LabelFrame(self.root, text=" Nova senha ", padding=(16, 10, 16, 14))
        cadastro.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 12))
        cadastro.columnconfigure(0, weight=1)
        ttk.Label(cadastro, text="Nome do cliente", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 5))
        ttk.Label(cadastro, text="Tipo de atendimento", style="Card.TLabel").grid(row=0, column=1, sticky="w", padx=(12, 0), pady=(0, 5))
        self.entrada_nome = ttk.Entry(cadastro, textvariable=self.nome)
        self.entrada_nome.grid(row=1, column=0, sticky="ew")
        self.entrada_nome.bind("<Return>", lambda _: self.cadastrar())
        ttk.Combobox(cadastro, textvariable=self.prioridade, values=("Normal", "Prioritário"),
                     state="readonly", width=16).grid(row=1, column=1, sticky="ew", padx=12)
        self.botao_cadastrar = ttk.Button(cadastro, text="Gerar senha", command=self.cadastrar)
        self.botao_cadastrar.grid(row=1, column=2, sticky="ew")

        chamada = ttk.Frame(self.root, style="Card.TFrame", padding=(16, 12))
        chamada.grid(row=2, column=0, sticky="ew", padx=22, pady=(0, 12))
        chamada.columnconfigure(0, weight=1)
        ttk.Label(chamada, text="Próximo da fila", style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        self.proximo_texto = tk.StringVar()
        ttk.Label(chamada, textvariable=self.proximo_texto, style="Card.TLabel",
                  font=(self.fonte, 14, "bold"), wraplength=520).grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.botao_atender = ttk.Button(chamada, text="Chamar próximo", style="Primary.TButton", command=self.atender)
        self.botao_atender.grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))

        self.abas = ttk.Notebook(self.root)
        self.abas.grid(row=3, column=0, sticky="nsew", padx=22)
        fila = ttk.Frame(self.abas, style="Card.TFrame", padding=14)
        historico = ttk.Frame(self.abas, style="Card.TFrame", padding=14)
        self.abas.add(fila, text="Fila de espera")
        self.abas.add(historico, text="Histórico de atendimentos")
        for aba in (fila, historico):
            aba.rowconfigure(1, weight=1)
            aba.columnconfigure(0, weight=1)
        pesquisa = ttk.Frame(fila, style="Card.TFrame")
        pesquisa.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(pesquisa, text="Prioritários primeiro; ordem de chegada em cada tipo.", style="Muted.TLabel").pack(side="left")
        ttk.Entry(pesquisa, textvariable=self.busca, width=20).pack(side="right")
        ttk.Label(pesquisa, text="Buscar  ", style="Muted.TLabel").pack(side="right")
        self.tabela_fila = self._tabela(fila, ("posicao", "senha", "nome", "categoria"), ("POSIÇÃO", "SENHA", "CLIENTE", "TIPO"))
        self.tabela_fila.bind("<<TreeviewSelect>>", lambda _: self._botoes())
        acoes = ttk.Frame(fila, style="Card.TFrame")
        acoes.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.resumo_fila = tk.StringVar()
        ttk.Label(acoes, textvariable=self.resumo_fila, style="Muted.TLabel").pack(side="left")
        self.botao_cancelar = ttk.Button(acoes, text="Cancelar senha", command=self.cancelar)
        self.botao_cancelar.pack(side="right")
        self.botao_reclassificar = ttk.Button(acoes, text="Alterar prioridade", command=self.reclassificar)
        self.botao_reclassificar.pack(side="right", padx=(8, 8))
        ttk.Label(historico, text="Atendimentos mais recentes primeiro", style="Muted.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.tabela_historico = self._tabela(historico, ("senha", "nome", "categoria"), ("SENHA", "CLIENTE", "TIPO"))
        self.resumo_historico = tk.StringVar()
        ttk.Label(historico, textvariable=self.resumo_historico, style="Muted.TLabel").grid(row=2, column=0, sticky="w", pady=(10, 0))

        rodape = ttk.Frame(self.root, padding=(22, 10, 22, 14))
        rodape.grid(row=4, column=0, sticky="ew")
        rodape.columnconfigure(0, weight=1)
        self.indicadores = {chave: tk.StringVar(value="0") for chave in ("pendentes", "prioritarios", "atendidos", "cancelados")}
        self.resumo_geral = tk.StringVar()
        ttk.Label(rodape, textvariable=self.resumo_geral, foreground=CINZA).grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Label(rodape, textvariable=self.status, wraplength=640).grid(row=1, column=0, sticky="w")
        self.botao_desfazer = ttk.Button(rodape, text="Desfazer", command=lambda: self.reverter(False))
        self.botao_desfazer.grid(row=0, column=1, rowspan=2, padx=(12, 6))
        self.botao_refazer = ttk.Button(rodape, text="Refazer", command=lambda: self.reverter(True))
        self.botao_refazer.grid(row=0, column=2, rowspan=2)

    def _tabela(self, parent, colunas, titulos):
        quadro = ttk.Frame(parent, style="Card.TFrame")
        quadro.grid(row=1, column=0, sticky="nsew")
        tabela = ttk.Treeview(quadro, columns=colunas, show="headings", selectmode="browse", height=6)
        for coluna, titulo in zip(colunas, titulos):
            tabela.heading(coluna, text=titulo, anchor="w")
            largura = {"posicao": 85, "senha": 100, "nome": 380, "categoria": 160}[coluna]
            tabela.column(coluna, width=largura, minwidth=65, stretch=coluna == "nome", anchor="w")
        scrollbar = ttk.Scrollbar(quadro, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tabela.pack(fill="both", expand=True)
        tabela.tag_configure("par", background="#f6f8fa")
        tabela.tag_configure("prioritario", foreground=AZUL)
        return tabela

    def _botoes(self):
        selecionado = bool(self.tabela_fila.selection())
        for botao in (self.botao_reclassificar, self.botao_cancelar):
            botao.state(["!disabled" if selecionado else "disabled"])
        for botao, ativo in ((self.botao_atender, self.sistema.proximo() is not None),
                             (self.botao_desfazer, not self.sistema.desfazer.vazia()),
                             (self.botao_refazer, not self.sistema.refazer.vazia())):
            botao.state(["!disabled" if ativo else "disabled"])

    def atualizar(self):
        selecao = self.tabela_fila.selection()
        estatisticas = self.sistema.estatisticas()
        for chave, var in self.indicadores.items():
            var.set(str(estatisticas[chave]))
        for tabela in (self.tabela_fila, self.tabela_historico):
            tabela.delete(*tabela.get_children())
        termo = self.busca.get().strip().casefold()
        visiveis = 0
        for i, c in enumerate(self.sistema.fila_ordenada(), 1):
            if termo and termo not in c.nome.casefold() and termo not in c.senha.casefold():
                continue
            tags = ("par",) if i % 2 == 0 else ()
            if c.prioritario:
                tags += ("prioritario",)
            self.tabela_fila.insert("", "end", iid=c.senha, values=(f"{i:02d}", c.senha, c.nome, c.categoria), tags=tags)
            visiveis += 1
        if selecao and self.tabela_fila.exists(selecao[0]):
            self.tabela_fila.selection_set(selecao)
        for i, c in enumerate(self.sistema.atendidos()):
            self.tabela_historico.insert("", "end", values=(c.senha, c.nome, c.categoria), tags=("par",) if i % 2 else ())
        self.resumo_fila.set(f"{visiveis} de {estatisticas['pendentes']} clientes exibidos • {estatisticas['normais']} normais")
        self.resumo_historico.set(f"{estatisticas['atendidos']} atendimentos registrados nesta sessão.")
        proximo = self.sistema.proximo()
        self.proximo_texto.set(f"{proximo.senha}  •  {proximo.nome}" if proximo else "Nenhum cliente em espera")
        self.resumo_geral.set(f"Aguardando: {estatisticas['pendentes']}    |    Prioritários: {estatisticas['prioritarios']}    |    Atendidos: {estatisticas['atendidos']}    |    Cancelados: {estatisticas['cancelados']}")
        self._botoes()
        self.root.title(f"Central de Atendimento Bancário{' • alterações não salvas' if self.alterado else ''}")

    def _mudou(self, texto):
        self.alterado = True
        self.status.set(texto)
        self.atualizar()

    def cadastrar(self):
        try:
            c = self.sistema.cadastrar(self.nome.get(), self.prioridade.get() == "Prioritário")
        except ValueError as erro:
            messagebox.showerror("Cadastro inválido", str(erro), parent=self.root)
            return
        self.nome.set("")
        self._mudou(f"Senha {c.senha} gerada para {c.nome}.")
        self.entrada_nome.focus_set()

    def atender(self):
        c = self.sistema.atender()
        if c is not None:
            self._mudou(f"Atendimento registrado: {c.senha} • {c.nome}.")

    def reverter(self, refazer):
        c = self.sistema.refazer_ultimo() if refazer else self.sistema.desfazer_ultimo()
        if c is not None:
            self._mudou(f"Operação {'refeita' if refazer else 'desfeita'}: {c.senha}.")

    def _selecionado(self):
        selecao = self.tabela_fila.selection()
        return self.sistema.buscar_pendente(selecao[0]) if selecao else None

    def reclassificar(self):
        c = self._selecionado()
        if c is None:
            return
        destino = "Normal" if c.prioritario else "Prioritário"
        if messagebox.askyesno("Alterar prioridade", f"Alterar {c.senha} — {c.nome} para {destino}?\nA senha será mantida.", parent=self.root):
            self.sistema.reclassificar(c.senha, not c.prioritario)
            self._mudou(f"{c.senha}: categoria alterada para {destino}.")

    def cancelar(self):
        c = self._selecionado()
        if c is not None and messagebox.askyesno("Cancelar senha", f"Retirar {c.senha} — {c.nome} da fila?\nEsta ação não pode ser desfeita.", parent=self.root):
            self.sistema.cancelar(c.senha)
            self._mudou(f"Senha {c.senha} cancelada.")

    def salvar(self):
        caminho = filedialog.asksaveasfilename(parent=self.root, title="Salvar sessão", defaultextension=".json",
                                              initialfile="sessao_bancaria.json", filetypes=[("Sessão JSON", "*.json")])
        if not caminho:
            return False
        try:
            salvar_sessao(self.sistema, caminho)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self.root)
            return False
        self.caminho = Path(caminho)
        self.alterado = False
        self.status.set(f"Sessão salva: {self.caminho.name}.")
        self.atualizar()
        return True

    def _confirmar_perda(self):
        if not self.alterado:
            return True
        resposta = messagebox.askyesnocancel("Alterações não salvas", "Salvar as alterações antes de continuar?", parent=self.root)
        if resposta is None:
            return False
        return self.salvar() if resposta else True

    def abrir(self):
        caminho = filedialog.askopenfilename(parent=self.root, title="Abrir sessão", filetypes=[("Sessão JSON", "*.json")])
        if not caminho:
            return
        try:
            novo = carregar_sessao(caminho)
        except (ValueError, OSError) as erro:
            messagebox.showerror("Sessão inválida", str(erro), parent=self.root)
            return
        if not self._confirmar_perda():
            return
        self.sistema = novo
        self.caminho = Path(caminho)
        self.alterado = False
        self.busca.set("")
        self.status.set(f"Sessão aberta: {self.caminho.name}. Pilhas de reversão reiniciadas.")
        self.atualizar()

    def exportar(self):
        caminho = filedialog.asksaveasfilename(parent=self.root, title="Exportar relatório", defaultextension=".csv",
                                              initialfile="relatorio_atendimento.csv", filetypes=[("Relatório CSV", "*.csv")])
        if caminho:
            try:
                exportar_csv(self.sistema, caminho)
            except OSError as erro:
                messagebox.showerror("Erro na exportação", str(erro), parent=self.root)
                return
            self.status.set(f"Relatório exportado: {Path(caminho).name}.")

    def demonstracao(self):
        if not self._confirmar_perda():
            return
        self.sistema = SistemaBancario()
        preencher_demonstracao(self.sistema)
        self.caminho = None
        self.busca.set("")
        self._mudou("Demonstração carregada com clientes fictícios.")

    def fechar(self):
        if self._confirmar_perda():
            self.root.destroy()


def executar(demo=False):
    try:
        root = tk.Tk()
    except tk.TclError as erro:
        raise SystemExit("Não foi possível abrir a janela. Execute em um ambiente gráfico com Tkinter disponível.") from erro
    banco = SistemaBancario()
    if demo:
        preencher_demonstracao(banco)
    app = AplicacaoBancaria(root, banco)
    if demo:
        app._mudou("Modo demonstração • clientes fictícios.")
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interface gráfica do atendimento bancário")
    parser.add_argument("--demo", action="store_true", help="iniciar com clientes fictícios")
    executar(parser.parse_args().demo)

