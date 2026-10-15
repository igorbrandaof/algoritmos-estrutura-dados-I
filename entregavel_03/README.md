# 3 — TAD Lista

## Objetivo
Listas sequencial, simples, dupla e circular

## Implementação e interface
ListaSequencial implementa inserir, remover, buscar e percorrer em vetor de capacidade fixa. ListaSimples implementa as mesmas operações com nós. ListaDupla mantém referências anterior/próximo e permite percurso reverso. ListaCircular liga o último nó ao primeiro.

## Execução
Na raiz, execute `python entregavel_03/demo.py`. Dentro desta pasta, use `python demo.py`.

## Testes
`python -m unittest discover -s . -p "testes*.py" -v`

## Complexidade
Sequencial: inserir/remover em posição O(n), busca O(n), acesso por índice O(1). Simples: inserir/remover por índice O(n), busca O(n), percurso O(n). Dupla: inserir/remover no fim O(1), busca O(n). Circular: inserir no fim e remover no início O(1), busca O(n).

## Limitações e decisões
Lista dupla e circular possuem interfaces complementares específicas. A lista sequencial usa um vetor de capacidade definida no construtor.


## Validação ampliada

9 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_03 -p "testes*.py" -v`.
