from dataclasses import dataclass
@dataclass(frozen=True)
class Cliente:
 nome: str
 senha: str
 prioritario: bool
 def __str__(self):
  return f'{self.senha} | {self.nome} | {"PRIORITARIO" if self.prioritario else "NORMAL"}'
