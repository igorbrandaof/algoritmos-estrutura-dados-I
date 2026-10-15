# Especificação do TAD SistemaBancario

## Estado e invariantes

- Cada cliente possui nome normalizado (1 a 100 caracteres), senha única, prioridade booleana e ordem de chegada positiva.
- Senhas N/P têm sequências independentes; números não são reutilizados após cancelamento.
- Cada cliente ativo está em exatamente uma fila ou no histórico.
- As filas são ordenadas pela chegada dentro da categoria. O histórico segue a ordem inversa dos atendimentos.
- `cadastrados = pendentes + atendidos + cancelados`.
- Na fila vazia, início e fim são `None`. Na fila não vazia, fim aponta para o último nó, cujo próximo é `None`.
- As pilhas guardam comandos imutáveis, não cópias completas do estado.

## Contratos públicos

| Método | Entrada / pré-condição | Resultado / pós-condição |
|---|---|---|
| `cadastrar(nome, prioritario=False)` | Nome não vazio; prioridade booleana | Cliente; nova senha; entra no fim; limpa ambas as pilhas |
| `proximo()` | Nenhuma | Cliente prioritário da frente, ou normal; `None` se vazio; não muta |
| `atender()` | Nenhuma | Move próximo para início do histórico e empilha comando; `None` se vazio |
| `reclassificar(senha, prioritario)` | Cliente pendente; prioridade booleana | Troca categoria mantendo identificação/chegada; empilha comando; mesma categoria é no-op |
| `cancelar(senha)` | Nenhuma | Remove pendente; incrementa cancelados e limpa pilhas; `None` se não encontrado |
| `desfazer_ultimo()` | Nenhuma | Reverte último atendimento/reclassificação; transfere comando para refazer; `None` se vazio |
| `refazer_ultimo()` | Nenhuma | Reaplica último comando desfeito; transfere para desfazer; `None` se vazio |
| `buscar_pendente(senha)` | Identificação | Cliente em espera ou `None`; ignora caixa/espaços externos |
| `consultar_atendimento(senha)` | Identificação | Cliente no histórico ou `None` |
| `pesquisar(termo, historico=False)` | Texto | Tupla com correspondência parcial em nome/senha; não muda fila |
| `filas()` | Nenhuma | Tuplas (prioritários, normais) |
| `fila_ordenada()` / `atendidos()` | Nenhuma | Tuplas para leitura; não expõem nós |
| `estatisticas()` | Nenhuma | Contadores de pendentes, categorias, atendidos, cancelados e cadastrados |

Dados inválidos de cadastro/reclassificação geram `ValueError`. Inconsistências internas de reversão geram `RuntimeError`, pois sinalizam quebra de invariantes.

## Exemplo verificável

```python
from projeto_final.sistema import SistemaBancario

b = SistemaBancario()
a = b.cadastrar("Ana")             # N001, chegada 1
b.cadastrar("Bia", True)            # P001, chegada 2
b.reclassificar(a.senha, True)       # N001 continua N001, agora prioritária
assert b.proximo().senha == "N001"  # chegada original preservada
b.atender()
b.desfazer_ultimo()                  # desfaz atendimento
b.desfazer_ultimo()                  # desfaz reclassificação
assert b.proximo().senha == "P001"
```

## Persistência

Esquema JSON versão 1: `versao`, `contadores`, `normal`, `prioritaria`, `historico`. Cada cliente é registrado com `nome`, `senha`, `prioritario`, `ordem`. Pilhas não são serializadas.

O carregador verifica versão, tipos, limites, duplicatas, contadores, categoria e FIFO antes de construir um novo sistema. A GUI substitui a sessão atual somente depois dessa validação e da decisão sobre alterações não salvas.
