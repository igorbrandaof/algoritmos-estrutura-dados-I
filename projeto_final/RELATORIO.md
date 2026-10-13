# Relatório técnico — Projeto final — Atendimento Bancário

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** [preencher]  
**Professor:** [preencher]

## 1. Objetivo
Integração de fila, lista e pilha.

## 2. Tipo abstrato de dados e interface
O sistema gera senhas N001/P001, mantém duas filas encadeadas, atende primeiro prioritários e registra atendimentos em lista encadeada. Uma pilha registra atendimentos reversíveis. O menu inclui cadastro, atendimento, visualização de filas, histórico, desfazer e consulta por senha.

## 3. Análise de complexidade
Cadastro: O(1); atender: O(1); desfazer: O(1); exibir filas/histórico: O(n); consultar histórico por senha: O(n). Espaço total O(n).

## 4. Procedimento de teste
Executar python main.py e python -m unittest testes.py -v. Verificar prioridade, FIFO, desfazer múltiplos atendimentos, cadastro após atendimento, fila vazia e entradas inválidas.

## 5. Discussão técnica
Regra de reversão: um novo cadastro invalida a pilha de desfazer, preservando o histórico. Isso evita reverter uma operação após alterações de fila não cobertas pela pilha. Dados são voláteis e não representam um banco real.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.
