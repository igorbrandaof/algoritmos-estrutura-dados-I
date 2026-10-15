"""Fila, pilha e lista encadeadas implementadas com nós, sem deque/list internos."""


class No:
    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class Fila:
    def __init__(self):
        self.inicio = self.fim = None
        self.quantidade = 0

    def vazia(self):
        return self.inicio is None

    def enfileirar(self, valor):
        no = No(valor)
        if self.fim:
            self.fim.proximo = no
        else:
            self.inicio = no
        self.fim = no
        self.quantidade += 1

    def colocar_na_frente(self, valor):
        self.inicio = No(valor, self.inicio)
        if self.fim is None:
            self.fim = self.inicio
        self.quantidade += 1

    def desenfileirar(self):
        if self.vazia():
            return None
        valor = self.inicio.valor
        self.inicio = self.inicio.proximo
        self.quantidade -= 1
        if self.inicio is None:
            self.fim = None
        return valor

    def frente(self):
        return None if self.vazia() else self.inicio.valor

    def remover(self, senha):
        """Remove por identificação; atualiza ambas as extremidades em O(n)."""
        anterior, atual = None, self.inicio
        while atual:
            if atual.valor.senha == senha:
                if anterior:
                    anterior.proximo = atual.proximo
                else:
                    self.inicio = atual.proximo
                if atual is self.fim:
                    self.fim = anterior
                self.quantidade -= 1
                return atual.valor
            anterior, atual = atual, atual.proximo
        return None

    def inserir_por_ordem(self, cliente):
        """Usado na reclassificação: preserva a ordem original de chegada."""
        anterior, atual = None, self.inicio
        while atual and atual.valor.ordem < cliente.ordem:
            anterior, atual = atual, atual.proximo
        no = No(cliente, atual)
        if anterior:
            anterior.proximo = no
        else:
            self.inicio = no
        if atual is None:
            self.fim = no
        self.quantidade += 1

    def __iter__(self):
        atual = self.inicio
        while atual:
            yield atual.valor
            atual = atual.proximo


class Pilha:
    def __init__(self):
        self._topo = None
        self.quantidade = 0

    def vazia(self):
        return self._topo is None

    def empilhar(self, valor):
        self._topo = No(valor, self._topo)
        self.quantidade += 1

    def desempilhar(self):
        if self.vazia():
            return None
        valor = self._topo.valor
        self._topo = self._topo.proximo
        self.quantidade -= 1
        return valor

    def limpar(self):
        self._topo = None
        self.quantidade = 0

    def topo(self):
        return None if self.vazia() else self._topo.valor


class ListaHistorico:
    def __init__(self):
        self.inicio = None
        self.quantidade = 0

    def inserir_inicio(self, valor):
        self.inicio = No(valor, self.inicio)
        self.quantidade += 1

    def remover_inicio(self):
        if self.inicio is None:
            return None
        valor = self.inicio.valor
        self.inicio = self.inicio.proximo
        self.quantidade -= 1
        return valor

    def buscar(self, senha):
        return next((cliente for cliente in self if cliente.senha == senha), None)

    def __iter__(self):
        atual = self.inicio
        while atual:
            yield atual.valor
            atual = atual.proximo
