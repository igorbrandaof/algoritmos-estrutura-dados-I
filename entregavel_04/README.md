# 4 — TAD Pilha

## Objetivo
LIFO e aplicação de balanceamento

## Implementação e interface
PilhaArray utiliza vetor prealocado com limite de capacidade; PilhaEncadeada utiliza nós. Ambas expõem push, pop, topo e vazia. A aplicação parenteses_balanceados verifica a correspondência de (), [] e {}.

## Execução
Na pasta deste módulo, execute `python demo.py` (módulos 1–5) ou `python main.py` (projeto final).

## Testes
`python -m unittest testes.py -v`

## Complexidade
push, pop, topo e vazia: O(1) em ambas. Balanceamento: O(n) tempo e O(n) espaço no pior caso.

## Limitações e decisões
A aplicação ignora caracteres que não sejam delimitadores. Em expressões reais, o analisador precisaria distinguir strings e comentários.
