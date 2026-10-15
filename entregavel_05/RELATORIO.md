# Relatório técnico — 5 — TAD Fila

**Curso:** Engenharia de Software  
**Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** Igor Fillipe Brandão Machado  
**Professor:** George Mendes Marra

## 1. Objetivo
FIFO, circularidade, prioridade e simulação.

## 2. Tipo abstrato de dados e interface
FilaCircular implementa índices modulares sobre vetor fixo; FilaEncadeada mantém início e fim; FilaPrioridade usa duas filas encadeadas com prioridade estrita. A simulação demonstra atendimento de clientes normais e prioritários.

## 3. Análise de complexidade
Enfileirar, desenfileirar, frente e vazia: O(1) em ambas as filas. Prioridade estrita: O(1) por atendimento; armazenamento O(n).

## 4. Procedimento de teste
Executar python demo.py e python -m unittest testes.py -v. Testar wrap-around, fila vazia, ordem de chegada e prioridade.

## 5. Discussão técnica
Prioridade estrita pode gerar espera indefinida para clientes normais; uma versão real precisaria de regras de justiça e conformidade normativa.

## 6. Conclusão
A implementação permite comparar custos de operações e compreender como a representação interna influencia o comportamento do TAD. As estruturas foram construídas explicitamente para fins didáticos, em vez de depender das coleções prontas da biblioteca padrão.


## Validação ampliada

8 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_05 -p "testes*.py" -v`.
