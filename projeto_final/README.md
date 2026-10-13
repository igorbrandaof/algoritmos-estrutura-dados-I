# Projeto final — Atendimento Bancário

## Objetivo
Integração de fila, lista e pilha

## Implementação e interface
O sistema gera senhas N001/P001, mantém duas filas encadeadas, atende primeiro prioritários e registra atendimentos em lista encadeada. Uma pilha registra atendimentos reversíveis. O menu inclui cadastro, atendimento, visualização de filas, histórico, desfazer e consulta por senha.

## Execução
Na pasta deste módulo, execute `python demo.py` (módulos 1–5) ou `python main.py` (projeto final).

## Testes
`python -m unittest testes.py -v`

## Complexidade
Cadastro: O(1); atender: O(1); desfazer: O(1); exibir filas/histórico: O(n); consultar histórico por senha: O(n). Espaço total O(n).

## Limitações e decisões
Regra de reversão: um novo cadastro invalida a pilha de desfazer, preservando o histórico. Isso evita reverter uma operação após alterações de fila não cobertas pela pilha. Dados são voláteis e não representam um banco real.
