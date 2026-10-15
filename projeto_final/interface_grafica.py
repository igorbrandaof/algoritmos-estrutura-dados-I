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
        self.root.title("Banco Acadêmico • Atendimento")
        self.root.geometry("1240x820")
        self.root.minsize(1060, 740)
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
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("TLabel", background=FUNDO, foreground=TEXTO, font=(self.fonte, 10))
        estilo.configure("Card.TLabel", background="white", foreground=TEXTO)
        estilo.configure("Muted.TLabel", background="white", foreground=CINZA, font=(self.fonte, 9))
        estilo.configure("Title.TLabel", background="white", font=(self.fonte, 15, "bold"))
        estilo.configure("TButton", font=(self.fonte, 10), padding=(12, 9), background="white", foreground=TEXTO)
        estilo.map("TButton", background=[("active", "#e8edf5")], foreground=[("disabled", "#a2acbb")])
        estilo.configure("Primary.TButton", background=VERDE, foreground="white", borderwidth=0)
        estilo.map("Primary.TButton", background=[("disabled", "#c2d6d2"), ("active", "#086b5f")],
                   foreground=[("disabled", "#617d77")])
        estilo.configure("TEntry", padding=8, fieldbackground="white")
        estilo.configure("TCombobox", padding=8, fieldbackground="white")
        estilo.configure("Treeview", background="white", fieldbackground="white", foreground=TEXTO,
                         rowheight=40, font=(self.fonte, 10), borderwidth=0)
        estilo.configure("Treeview.Heading", background="#eef2f7", foreground=CINZA,
                         padding=12, font=(self.fonte, 9, "bold"), relief="flat")
        estilo.map("Treeview", background=[("selected", "#d6eee8")], foreground=[("selected", AZUL)])
        estilo.configure("TNotebook", background=FUNDO, borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(18, 11), font=(self.fonte, 10))
        estilo.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", VERDE)])

    def _construir(self):
        cabecalho = tk.Frame(self.root, bg=AZUL, padx=26, pady=18)
        cabecalho.grid(row=0, column=0, sticky="ew")
        tk.Label(cabecalho, text="B /  BANCO ACADÊMICO", bg=AZUL, fg="white",
                 font=(self.fonte, 17, "bold")).pack(side="left")
        tk.Label(cabecalho, text="AED I   •   SIMULAÇÃO EDUCACIONAL", bg=AZUL, fg="#b7cadf",
                 font=(self.fonte, 9)).pack(side="right")
        barra = ttk.Frame(self.root, padding=(24, 16, 24, 12))
        barra.grid(row=1, column=0, sticky="ew")
        ttk.Label(barra, text="Central de atendimento", font=(self.fonte, 20, "bold")).pack(side="left")
        for rotulo, comando in (("Exportar CSV", self.exportar), ("Salvar sessão", self.salvar), ("Abrir sessão", self.abrir)):
            ttk.Button(barra, text=rotulo, command=comando).pack(side="right", padx=(6, 0))
        indicadores = ttk.Frame(self.root, padding=(24, 0, 24, 16))
        indicadores.grid(row=2, column=0, sticky="ew")
        self.indicadores = {}
        for i, (chave, rotulo, cor) in enumerate((("pendentes", "NA FILA", AZUL), ("prioritarios", "PRIORITÁRIOS", VERDE),
                                               ("atendidos", "ATENDIDOS", AZUL), ("cancelados", "CANCELADOS", CINZA))):
            indicadores.columnconfigure(i, weight=1, uniform="cards")
            card = ttk.Frame(indicadores, style="Card.TFrame", padding=(18, 12))
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
            ttk.Label(card, text=rotulo, style="Muted.TLabel").pack(anchor="w")
            valor = tk.StringVar(value="0")
            tk.Label(card, textvariable=valor, bg="white", fg=cor, font=(self.fonte, 26, "bold")).pack(anchor="w")
            self.indicadores[chave] = valor
        conteudo = ttk.Frame(self.root, padding=(24, 0, 24, 0))
        conteudo.grid(row=3, column=0, sticky="nsew")
        lateral = ttk.Frame(conteudo, style="Card.TFrame", padding=16, width=290)
        lateral.pack(side="left", fill="y", padx=(0, 16))
        lateral.pack_propagate(False)
        self.botao_demo = ttk.Button(lateral, text="Carregar demonstração", command=self.demonstracao)
        self.botao_demo.pack(side="bottom", fill="x", pady=(0, 4))
        ttk.Label(lateral, text="Novo cliente", style="Title.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(lateral, text="Gere uma senha e entre na fila.", style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(lateral, text="Nome completo", style="Card.TLabel").pack(anchor="w")
        self.entrada_nome = ttk.Entry(lateral, textvariable=self.nome)
        self.entrada_nome.pack(fill="x", pady=(6, 10))
        self.entrada_nome.bind("<Return>", lambda _: self.cadastrar())
        ttk.Label(lateral, text="Categoria de atendimento", style="Card.TLabel").pack(anchor="w")
        ttk.Combobox(lateral, textvariable=self.prioridade, values=("Normal", "Prioritário"), state="readonly").pack(fill="x", pady=(6, 16))
        ttk.Button(lateral, text="+  Cadastrar cliente", style="Primary.TButton", command=self.cadastrar).pack(fill="x")
        ttk.Separator(lateral).pack(fill="x", pady=10)
        ttk.Label(lateral, text="Como funciona", style="Card.TLabel", font=(self.fonte, 11, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(lateral, text="Cadastre → confira a fila.\nChame o próximo → histórico.",
                  style="Muted.TLabel", justify="left").pack(anchor="w")
        ttk.Label(lateral, text="Prioridade estrita, com FIFO\nem cada categoria.",
                  style="Muted.TLabel", justify="left").pack(anchor="w", pady=(12, 0))
        direita = ttk.Frame(conteudo)
        direita.pack(side="left", fill="both", expand=True)
        direita.rowconfigure(0, weight=1)
        direita.columnconfigure(0, weight=1)
        self.abas = ttk.Notebook(direita)
        self.abas.grid(row=0, column=0, sticky="nsew")
        fila = ttk.Frame(self.abas, style="Card.TFrame", padding=16)
        historico = ttk.Frame(self.abas, style="Card.TFrame", padding=16)
        didatica = ttk.Frame(self.abas, style="Card.TFrame", padding=18)
        self.abas.add(fila, text="Fila de espera")
        self.abas.add(historico, text="Histórico")
        self.abas.add(didatica, text="Estruturas de dados")
        for aba in (fila, historico):
            aba.rowconfigure(1, weight=1)
            aba.columnconfigure(0, weight=1)
        pesquisa = ttk.Frame(fila, style="Card.TFrame")
        pesquisa.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(pesquisa, text="Ordem real de atendimento", style="Card.TLabel", font=(self.fonte, 11, "bold")).pack(side="left")
        ttk.Entry(pesquisa, textvariable=self.busca, width=23).pack(side="right")
        ttk.Label(pesquisa, text="Buscar nome ou senha  ", style="Muted.TLabel").pack(side="right")
        self.tabela_fila = self._tabela(fila, ("posicao", "senha", "nome", "categoria"), ("POSIÇÃO", "SENHA", "CLIENTE", "CATEGORIA"))
        self.tabela_fila.bind("<<TreeviewSelect>>", lambda _: self._botoes())
        self.resumo_fila = tk.StringVar()
        ttk.Label(fila, textvariable=self.resumo_fila, style="Muted.TLabel").grid(row=2, column=0, sticky="w", pady=(8, 10))
        acoes = ttk.Frame(fila, style="Card.TFrame")
        acoes.grid(row=3, column=0, sticky="ew")
        self.botao_reclassificar = ttk.Button(acoes, text="Alterar prioridade", command=self.reclassificar)
        self.botao_reclassificar.pack(side="left")
        self.botao_cancelar = ttk.Button(acoes, text="Cancelar senha", command=self.cancelar)
        self.botao_cancelar.pack(side="left", padx=8)
        ttk.Label(historico, text="Atendimentos • mais recente primeiro", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.tabela_historico = self._tabela(historico, ("senha", "nome", "categoria"), ("SENHA", "CLIENTE", "CATEGORIA"))
        self.resumo_historico = tk.StringVar()
        ttk.Label(historico, textvariable=self.resumo_historico, style="Muted.TLabel").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Label(didatica, text="O que acontece por trás da tela", style="Title.TLabel").pack(anchor="w", pady=(0, 16))
        self.estruturas_texto = tk.StringVar()
        self.texto_didatico = tk.Text(didatica, wrap="word", bg="white", fg=TEXTO, relief="flat",
                                      font=(self.fonte, 11), height=10, padx=4, pady=4)
        rolagem_didatica = ttk.Scrollbar(didatica, orient="vertical", command=self.texto_didatico.yview)
        self.texto_didatico.configure(yscrollcommand=rolagem_didatica.set)
        rolagem_didatica.pack(side="right", fill="y")
        self.texto_didatico.pack(fill="both", expand=True)
        chamada = ttk.Frame(direita, style="Card.TFrame", padding=(16, 12))
        chamada.grid(row=1, column=0, sticky="ew", pady=(14, 0))
        bloco = ttk.Frame(chamada, style="Card.TFrame")
        bloco.pack(side="left", fill="x", expand=True)
        ttk.Label(bloco, text="PRÓXIMO ATENDIMENTO", style="Muted.TLabel").pack(anchor="w")
        self.proximo_texto = tk.StringVar()
        ttk.Label(bloco, textvariable=self.proximo_texto, style="Title.TLabel", wraplength=430).pack(anchor="w", pady=(4, 0))
        self.botao_atender = ttk.Button(chamada, text="Chamar próximo  →", style="Primary.TButton", command=self.atender)
        self.botao_atender.pack(side="right")
        rodape = ttk.Frame(self.root, padding=(24, 12))
        rodape.grid(row=4, column=0, sticky="ew")
        self.botao_desfazer = ttk.Button(rodape, text="↶ Desfazer", command=lambda: self.reverter(False))
        self.botao_desfazer.pack(side="left")
        self.botao_refazer = ttk.Button(rodape, text="↷ Refazer", command=lambda: self.reverter(True))
        self.botao_refazer.pack(side="left", padx=8)
        ttk.Label(rodape, textvariable=self.status, wraplength=650, foreground=CINZA).pack(side="left", padx=14)

    def _tabela(self, parent, colunas, titulos):
        quadro = ttk.Frame(parent, style="Card.TFrame")
        quadro.grid(row=1, column=0, sticky="nsew")
        tabela = ttk.Treeview(quadro, columns=colunas, show="headings", selectmode="browse", height=6)
        for coluna, titulo in zip(colunas, titulos):
            tabela.heading(coluna, text=titulo, anchor="w")
            largura = {"posicao": 80, "senha": 90, "nome": 280, "categoria": 135}[coluna]
            tabela.column(coluna, width=largura, minwidth=65, stretch=coluna == "nome", anchor="w")
        scrollbar = ttk.Scrollbar(quadro, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tabela.pack(fill="both", expand=True)
        tabela.tag_configure("par", background="#f7f9fc")
        tabela.tag_configure("prioritario", foreground=VERDE)
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
        p = " → ".join(c.senha for c in self.sistema.prioritaria) or "vazia"
        n = " → ".join(c.senha for c in self.sistema.normal) or "vazia"
        self.estruturas_texto.set(
            f"FILA FIFO • encadeada, entrada no fim e saída no início\nPrioritários: {p}\nNormais: {n}\n\n"
            f"LISTA ENCADEADA • histórico com inserção no início\n{estatisticas['atendidos']} registros; busca linear O(n).\n\n"
            f"DUAS PILHAS LIFO • comandos inversos para desfazer/refazer\n"
            f"Desfazer: {self.sistema.desfazer.quantidade}  |  Refazer: {self.sistema.refazer.quantidade}\n\n"
            "A interface percorre as estruturas do núcleo. A tabela não decide quem será chamado.")
        self.texto_didatico.configure(state="normal")
        self.texto_didatico.delete("1.0", "end")
        self.texto_didatico.insert("1.0", self.estruturas_texto.get() + "\n\nOS CINCO ENTREGÁVEIS\n\n"
                                  "01  Funções, parâmetros e recursividade\n"
                                  "02  TAD Conta Bancária e armazenamento\n"
                                  "03  Listas sequenciais e encadeadas\n"
                                  "04  Pilhas e balanceamento de delimitadores\n"
                                  "05  Filas circulares, encadeadas e prioritárias")
        self.texto_didatico.configure(state="disabled")
        self._botoes()
        self.root.title(f"Banco Acadêmico • Atendimento{' • alterações não salvas' if self.alterado else ''}")

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
