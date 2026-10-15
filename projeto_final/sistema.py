"""Núcleo compartilhado: prioridade estrita, FIFO e operações reversíveis.

Cadastro/cancelamento iniciam uma nova sequência de reversão. Atendimento e
reclassificação usam duas pilhas encadeadas de comandos inversos (undo/redo).
"""
from dataclasses import dataclass, replace

if __package__:
    from .cliente import Cliente
    from .estruturas import Fila, Pilha, ListaHistorico
else:
    from cliente import Cliente
    from estruturas import Fila, Pilha, ListaHistorico


@dataclass(frozen=True)
class Operacao:
    tipo: str
    antes: Cliente
    depois: Cliente | None = None


class SistemaBancario:
    def __init__(self):
        self.normal = Fila()
        self.prioritaria = Fila()
        self.historico = ListaHistorico()
        self.desfazer = Pilha()
        self.refazer = Pilha()
        self._seq_normal = self._seq_prioritaria = self._ordem = 0
        self.cancelados = 0

    def _fila(self, prioritario):
        return self.prioritaria if prioritario else self.normal

    def _limpar_reversoes(self):
        self.desfazer.limpar()
        self.refazer.limpar()

    def cadastrar(self, nome, prioritario=False):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Informe o nome do cliente.")
        nome = " ".join(nome.split())
        if len(nome) > 100:
            raise ValueError("O nome deve ter no máximo 100 caracteres.")
        if not isinstance(prioritario, bool):
            raise ValueError("A prioridade deve ser booleana.")
        if prioritario:
            self._seq_prioritaria += 1
            senha = f"P{self._seq_prioritaria:03d}"
        else:
            self._seq_normal += 1
            senha = f"N{self._seq_normal:03d}"
        self._ordem += 1
        cliente = Cliente(nome, senha, prioritario, self._ordem)
        self._fila(prioritario).enfileirar(cliente)
        self._limpar_reversoes()
        return cliente

    def proximo(self):
        return self.prioritaria.frente() or self.normal.frente()

    def atender(self):
        cliente = self.proximo()
        if cliente is None:
            return None
        self._fila(cliente.prioritario).desenfileirar()
        self.historico.inserir_inicio(cliente)
        self.desfazer.empilhar(Operacao("atendimento", cliente))
        self.refazer.limpar()
        return cliente

    def reclassificar(self, senha, prioritario):
        if not isinstance(prioritario, bool):
            raise ValueError("A prioridade deve ser booleana.")
        cliente = self.buscar_pendente(senha)
        if cliente is None:
            raise ValueError("Cliente não encontrado na fila de espera.")
        if cliente.prioritario == prioritario:
            return cliente
        novo = replace(cliente, prioritario=prioritario)
        self._trocar_categoria(cliente, novo)
        self.desfazer.empilhar(Operacao("reclassificacao", cliente, novo))
        self.refazer.limpar()
        return novo

    def _trocar_categoria(self, antes, depois):
        removido = self._fila(antes.prioritario).remover(antes.senha)
        if removido != antes:
            raise RuntimeError("Fila inconsistente na reclassificação.")
        self._fila(depois.prioritario).inserir_por_ordem(depois)

    def cancelar(self, senha):
        cliente = self.buscar_pendente(senha)
        if cliente is None:
            return None
        self._fila(cliente.prioritario).remover(cliente.senha)
        self.cancelados += 1
        self._limpar_reversoes()
        return cliente

    def desfazer_ultimo(self):
        operacao = self.desfazer.topo()
        if operacao is None:
            return None
        if operacao.tipo == "atendimento":
            if self.historico.inicio is None or self.historico.inicio.valor != operacao.antes:
                raise RuntimeError("Histórico inconsistente.")
            self.historico.remover_inicio()
            self._fila(operacao.antes.prioritario).colocar_na_frente(operacao.antes)
        else:
            self._trocar_categoria(operacao.depois, operacao.antes)
        self.desfazer.desempilhar()
        self.refazer.empilhar(operacao)
        return operacao.antes

    def refazer_ultimo(self):
        operacao = self.refazer.topo()
        if operacao is None:
            return None
        if operacao.tipo == "atendimento":
            if self.proximo() != operacao.antes:
                raise RuntimeError("Fila inconsistente ao refazer.")
            self._fila(operacao.antes.prioritario).desenfileirar()
            self.historico.inserir_inicio(operacao.antes)
        else:
            self._trocar_categoria(operacao.antes, operacao.depois)
        self.refazer.desempilhar()
        self.desfazer.empilhar(operacao)
        return operacao.depois or operacao.antes

    def filas(self):
        return tuple(self.prioritaria), tuple(self.normal)

    def fila_ordenada(self):
        return tuple(self.prioritaria) + tuple(self.normal)

    def atendidos(self):
        return tuple(self.historico)

    def buscar_pendente(self, senha):
        senha = str(senha).strip().upper()
        for fila in (self.prioritaria, self.normal):
            for cliente in fila:
                if cliente.senha == senha:
                    return cliente
        return None

    def consultar_atendimento(self, senha):
        return self.historico.buscar(str(senha).strip().upper())

    def pesquisar(self, termo="", historico=False):
        termo = termo.strip().casefold()
        origem = self.atendidos() if historico else self.fila_ordenada()
        return tuple(c for c in origem if termo in c.nome.casefold() or termo in c.senha.casefold())

    def pendentes(self):
        return self.prioritaria.quantidade + self.normal.quantidade

    def estatisticas(self):
        return {
            "pendentes": self.pendentes(),
            "prioritarios": self.prioritaria.quantidade,
            "normais": self.normal.quantidade,
            "atendidos": self.historico.quantidade,
            "cancelados": self.cancelados,
            "cadastrados": self._ordem,
        }
