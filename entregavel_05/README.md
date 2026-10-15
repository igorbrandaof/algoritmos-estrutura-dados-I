# 5 — TAD Fila

## Objetivo
FIFO, circularidade, prioridade e simulação

## Implementação e interface
FilaCircular implementa índices modulares sobre vetor fixo; FilaEncadeada mantém início e fim; FilaPrioridade usa duas filas encadeadas com prioridade estrita. A simulação demonstra atendimento de clientes normais e prioritários.

## Execução
Na raiz, execute `python entregavel_05/demo.py`. Dentro desta pasta, use `python demo.py`.

## Testes
`python -m unittest discover -s . -p "testes*.py" -v`

## Complexidade
Enfileirar, desenfileirar, frente e vazia: O(1) em ambas as filas. Prioridade estrita: O(1) por atendimento; armazenamento O(n).

## Limitações e decisões
Prioridade estrita pode gerar espera indefinida para clientes normais; uma versão real precisaria de regras de justiça e conformidade normativa.


## Validação ampliada

8 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_05 -p "testes*.py" -v`.
