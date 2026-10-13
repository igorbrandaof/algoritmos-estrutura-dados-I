# Relatório técnico — 1 — Biblioteca de funções

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** [preencher]  
**Professor:** [preencher]

## 1. Objetivo
Modularização, passagem de parâmetros e recursividade.

## 2. Tipo abstrato de dados e interface
A biblioteca utilitarios.py implementa fatorial, Fibonacci, busca binária recursiva, média, troca de valores e mutação de um contador. A demonstração de passagem por valor versus referência é contextualizada: em Python os argumentos são passados por atribuição de referências a objetos; inteiros são imutáveis e dicionários são mutáveis.

## 3. Análise de complexidade
fatorial: O(n) tempo e O(n) pilha; Fibonacci ingênuo: O(2^n) tempo e O(n) pilha; busca binária: O(log n) tempo e O(log n) pilha; média: O(n).

## 4. Procedimento de teste
Executar python demo.py e python -m unittest testes.py -v. Testar casos n=0, negativos, busca sem resultado e mutação de objeto.

## 5. Discussão técnica
O Fibonacci recursivo simples foi escolhido para evidenciar recursão, não para uso de alto desempenho. Busca binária exige vetor previamente ordenado.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.
