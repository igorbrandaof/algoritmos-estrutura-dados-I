"""Registro imutável: senha identifica o cliente mesmo após reclassificação."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    nome: str
    senha: str
    prioritario: bool
    ordem: int = 0

    @property
    def categoria(self):
        return "Prioritário" if self.prioritario else "Normal"

    def __str__(self):
        return f"{self.senha} | {self.nome} | {self.categoria.upper()}"
