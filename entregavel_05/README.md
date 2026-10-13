# 5 — TAD Fila

## Objetivo
FIFO, circularidade, prioridade e simulação

## Implementação e interface
FilaCircular implementa índices modulares sobre vetor fixo; FilaEncadeada mantém início e fim; FilaPrioridade usa duas filas encadeadas com prioridade estrita. A simulação demonstra atendimento de clientes normais e prioritários.

## Execução
Na pasta deste módulo, execute `python demo.py` (módulos 1–5) ou `python main.py` (projeto final).

## Testes
`python -m unittest testes.py -v`

## Complexidade
Enfileirar, desenfileirar, frente e vazia: O(1) em ambas as filas. Prioridade estrita: O(1) por atendimento; armazenamento O(n).

## Limitações e decisões
Prioridade estrita pode gerar espera indefinida para clientes normais; uma versão real precisaria de regras de justiça e conformidade normativa.
