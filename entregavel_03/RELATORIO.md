# Relatório técnico — 3 — TAD Lista

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** Igor Fillipe Brandão Machado  
**Professor:** George Mendes Marra

## 1. Objetivo
Listas sequencial, simples, dupla e circular.

## 2. Tipo abstrato de dados e interface
ListaSequencial implementa inserir, remover, buscar e percorrer em vetor de capacidade fixa. ListaSimples implementa as mesmas operações com nós. ListaDupla mantém referências anterior/próximo e permite percurso reverso. ListaCircular liga o último nó ao primeiro.

## 3. Análise de complexidade
Sequencial: inserir/remover em posição O(n), busca O(n), acesso por índice O(1). Simples: inserir/remover por índice O(n), busca O(n), percurso O(n). Dupla: inserir/remover no fim O(1), busca O(n). Circular: inserir no fim e remover no início O(1), busca O(n).

## 4. Procedimento de teste
Executar python demo.py e python -m unittest testes.py -v. Testar lista vazia, inserção intermediária, remoção, ordem reversa e fechamento circular.

## 5. Discussão técnica
Lista dupla e circular possuem interfaces complementares específicas. A lista sequencial usa um vetor de capacidade definida no construtor.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.


## Validação ampliada

9 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_03 -p "testes*.py" -v`.
