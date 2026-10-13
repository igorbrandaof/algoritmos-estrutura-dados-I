# 1 — Biblioteca de funções

## Objetivo
Modularização, passagem de parâmetros e recursividade

## Implementação e interface
A biblioteca utilitarios.py implementa fatorial, Fibonacci, busca binária recursiva, média, troca de valores e mutação de um contador. A demonstração de passagem por valor versus referência é contextualizada: em Python os argumentos são passados por atribuição de referências a objetos; inteiros são imutáveis e dicionários são mutáveis.

## Execução
Na pasta deste módulo, execute `python demo.py` (módulos 1–5) ou `python main.py` (projeto final).

## Testes
`python -m unittest testes.py -v`

## Complexidade
fatorial: O(n) tempo e O(n) pilha; Fibonacci ingênuo: O(2^n) tempo e O(n) pilha; busca binária: O(log n) tempo e O(log n) pilha; média: O(n).

## Limitações e decisões
O Fibonacci recursivo simples foi escolhido para evidenciar recursão, não para uso de alto desempenho. Busca binária exige vetor previamente ordenado.
