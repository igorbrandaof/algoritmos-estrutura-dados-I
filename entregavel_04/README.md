# 4 — TAD Pilha

## Objetivo
LIFO e aplicação de balanceamento

## Implementação e interface
PilhaArray utiliza vetor prealocado com limite de capacidade; PilhaEncadeada utiliza nós. Ambas expõem push, pop, topo e vazia. A aplicação parenteses_balanceados verifica a correspondência de (), [] e {}.

## Execução
Na raiz, execute `python entregavel_04/demo.py`. Dentro desta pasta, use `python demo.py`.

## Testes
`python -m unittest discover -s . -p "testes*.py" -v`

## Complexidade
push, pop, topo e vazia: O(1) em ambas. Balanceamento: O(n) tempo e O(n) espaço no pior caso.

## Limitações e decisões
A aplicação ignora caracteres que não sejam delimitadores. Em expressões reais, o analisador precisaria distinguir strings e comentários.


## Validação ampliada

7 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_04 -p "testes*.py" -v`.
