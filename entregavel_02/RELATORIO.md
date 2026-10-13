# Relatório técnico — 2 — TAD Conta Bancária

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** [preencher]  
**Professor:** [preencher]

## 1. Objetivo
Encapsulamento, capacidade fixa e objetos dinâmicos.

## 2. Tipo abstrato de dados e interface
Conta encapsula saldo com métodos depositar e sacar. BancoEstatico usa vetor de capacidade fixa e deslocamento na remoção. BancoDinamico usa nós ligados e criação sob demanda. Interface pública: inserir, buscar, remover e quantidade, além dos métodos da conta.

## 3. Análise de complexidade
BancoEstatico: inserir O(n) devido à checagem de duplicidade; buscar O(n); remover O(n). BancoDinamico: inserir O(n) com checagem de duplicidade; buscar O(n); remover O(n). Armazenamento O(n) em ambas.

## 4. Procedimento de teste
Executar python demo.py e python -m unittest testes.py -v. Testar depósito, saque, capacidade cheia, busca, exclusão e saldo insuficiente.

## 5. Discussão técnica
Em Python, o vetor é uma lista prealocada com tamanho fixo lógico, não uma alocação estática real de C. Os nós são objetos criados dinamicamente e liberados pelo coletor de lixo.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.
