# Roteiro para apresentação (10 a 15 minutos)

**0:00–1:00 — Abertura:** apresentar disciplina, objetivo e problema de organização de atendimentos.

**1:00–3:00 — Fundamentos:** explicar TAD, modularização, FIFO e LIFO; comparar arrays e nós encadeados.

**3:00–5:00 — Entregáveis 1–3:** mostrar funções recursivas, conta estática/dinâmica e listas.

**5:00–7:00 — Entregáveis 4–5:** mostrar pilha e fila circular/encadeada, com casos de uso.

**7:00–11:00 — Demonstração:** executar `python main.py`; cadastrar Ana (normal), Bia (prioritária), Caio (normal); exibir filas; atender Bia; consultar histórico; desfazer atendimento; atender novamente.

**11:00–13:00 — Complexidade:** atendimento, cadastro e desfazer O(1), consulta O(n). Explicar porque início/fim da fila evitam percorrer todos os nós.

**13:00–15:00 — Testes e limitações:** mostrar `python executar_testes.py`, discutir prioridade estrita, persistência e política de desfazer.

## Perguntas prováveis
**Por que usar fila?** Para garantir FIFO dentro de cada categoria.
**Por que pilha?** Para reverter atendimentos na ordem inversa.
**Por que lista encadeada?** Para histórico dinâmico com inserção O(1) no início.
**Python tem ponteiros?** Tem referências a objetos; nós ligados simulam encadeamento sem ponteiros explícitos.
**Por que desfazer limpa ao cadastrar?** Para evitar reversões inconsistentes após mudança não registrada na pilha.
