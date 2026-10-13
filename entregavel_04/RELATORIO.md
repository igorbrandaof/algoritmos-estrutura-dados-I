# Relatório técnico — 4 — TAD Pilha

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** [preencher]  
**Professor:** [preencher]

## 1. Objetivo
LIFO e aplicação de balanceamento.

## 2. Tipo abstrato de dados e interface
PilhaArray utiliza vetor prealocado com limite de capacidade; PilhaEncadeada utiliza nós. Ambas expõem push, pop, topo e vazia. A aplicação parenteses_balanceados verifica a correspondência de (), [] e {}.

## 3. Análise de complexidade
push, pop, topo e vazia: O(1) em ambas. Balanceamento: O(n) tempo e O(n) espaço no pior caso.

## 4. Procedimento de teste
Executar python demo.py e python -m unittest testes.py -v. Verificar ([{}]) como válido e ([)] como inválido.

## 5. Discussão técnica
A aplicação ignora caracteres que não sejam delimitadores. Em expressões reais, o analisador precisaria distinguir strings e comentários.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.
