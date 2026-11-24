"""Registro imutável: senha identifica o cliente mesmo após reclassificação."""
from dataclasses import dataclass

SERVICOS = {'Saque': 'Guichê rápido', 'Depósito': 'Guichê rápido', 'Impressão de extrato': 'Guichê rápido', 'Desbloqueio simples': 'Guichê rápido', 'Abertura de conta': 'Especialista', 'Cancelamento de conta': 'Especialista', 'Crédito': 'Especialista', 'Investimentos': 'Especialista', 'Renegociação': 'Especialista', 'Não informado': 'Triagem geral'}


@dataclass(frozen=True)
class Cliente:
    nome: str
    senha: str
    prioritario: bool
    ordem: int = 0
    servico: str = "Não informado"

    @property
    def destino(self):
        return SERVICOS[self.servico]

    @property
    def categoria(self):
        return "Prioritário" if self.prioritario else "Normal"

    def __str__(self):
        return f"{self.senha} | {self.nome} | {self.categoria.upper()} | {self.servico} | {self.destino}"
