# 2 — TAD Conta Bancária

## Objetivo
Encapsulamento, capacidade fixa e objetos dinâmicos

## Implementação e interface
Conta encapsula saldo com métodos depositar e sacar. BancoEstatico usa vetor de capacidade fixa e deslocamento na remoção. BancoDinamico usa nós ligados e criação sob demanda. Interface pública: inserir, buscar, remover e quantidade, além dos métodos da conta.

## Execução
Na pasta deste módulo, execute `python demo.py` (módulos 1–5) ou `python main.py` (projeto final).

## Testes
`python -m unittest testes.py -v`

## Complexidade
BancoEstatico: inserir O(n) devido à checagem de duplicidade; buscar O(n); remover O(n). BancoDinamico: inserir O(n) com checagem de duplicidade; buscar O(n); remover O(n). Armazenamento O(n) em ambas.

## Limitações e decisões
Em Python, o vetor é uma lista prealocada com tamanho fixo lógico, não uma alocação estática real de C. Os nós são objetos criados dinamicamente e liberados pelo coletor de lixo.
