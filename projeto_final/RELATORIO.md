# Relatório técnico — Sistema de Gerenciamento de Atendimento Bancário

**Curso:** Engenharia de Software · **Disciplina:** Algoritmos e Estrutura de Dados I  
**Aluno:** Igor Fillipe Brandão Machado · **Professor:** George Mendes Marra · **Instituição:** UNIALFA

## 1. Objetivo e escopo

Integrar estruturas de fila, lista e pilha em uma aplicação de atendimento bancário. O projeto original em Python foi estendido com interface gráfica, reclassificação reversível e persistência, mantendo os cinco entregáveis. Não há transações reais nem integração financeira.

## 2. Representações e contratos

Cliente é um registro imutável com nome, senha, categoria e ordem global de chegada. Duas filas encadeadas implementam prioridade estrita e FIFO por categoria. O histórico é uma lista encadeada com inserção no início. Duas pilhas encadeadas guardam comandos aplicados/desfeitos.

As estruturas usam nós manuais; list/deque não substituem seu armazenamento interno. Tuplas e listas temporárias são usadas apenas em leitura, serialização e validação. Contratos e invariantes estão em ESPECIFICACAO_TAD.md.

## 3. Fluxos e decisões

Cadastro valida nome/categoria, gera senha e enfileira. Atendimento retira o próximo prioritário (ou normal) e o insere no histórico. Reclassificação preserva senha/chegada e reinsere o registro na posição correta da categoria de destino.

Atendimento/reclassificação são reversíveis por comandos LIFO. Cadastro e cancelamento limpam as pilhas e preserva histórico, mantendo a regra do projeto original. Cancelamento não é reversível. Senha passa a ser identidade permanente, independente da categoria atual.

Terminal e Tkinter compartilham o mesmo SistemaBancario; a interface apenas apresenta dados e chama operações. Confirmações e proteção contra perda de alterações são responsabilidade da GUI, não das estruturas.

## 4. Persistência

JSON versão 1 salva filas, histórico, contadores e cancelamentos. Um novo sistema só é construído após validar tipos, nomes, senhas, ordens, duplicatas, categorias, FIFO e totais. Limite de entrada: 5 MB. Pilhas não são persistidas.

A escrita usa temporário no mesmo diretório, flush/fsync e replace atômico. CSV apresenta fila/histórico em UTF-8 com BOM, com delimitador ponto e vírgula e tratamento de nomes que poderiam ser interpretados como fórmulas.

## 5. Análise de complexidade

| Operação | Tempo | Espaço auxiliar |
|---|---|---|
| Cadastro e atendimento | O(1) nas estruturas; limpeza pode liberar O(h) nós | O(1) por registro/comando |
| Próximo e indicadores | O(1) | O(1) |
| Desfazer/refazer atendimento | O(1) | O(1) |
| Reclassificação e reversão | O(n) | O(1) na manipulação de nós |
| Cancelamento e busca por senha | O(n); cancelamento pode liberar O(h) comandos | O(1) |
| Pesquisa, listagem e renderização | O(n) | O(n) |
| JSON/CSV e abertura | O(n), abertura em média por conjuntos | O(n) |

Estado total O(n+h), com n clientes ativos/atendidos e h comandos de reversão. Objetos cancelados deixam as filas; o contador de cancelamento não mantém seus dados. Python gerencia liberação de memória e coleta de lixo.

## 6. Validação

Dez testes originais do projeto final foram preservados; 36 testes de domínio/persistência e 15 de widgets reais foram acrescentados. Com os entregáveis, são 107 testes locais. Os testes verificam comportamento e fronteiras: FIFO, reclassificação estável, comandos intercalados, invalidação de redo, contadores, arquivo corrompido, duplicatas, falha simulada de salvamento e atualização de tabelas/indicadores.

A GUI foi renderizada no Linux e inspecionada nas dimensões 1240×820 e 1060×740. A validação nativa em Windows/macOS permanece como limitação. Resultados completos em documentacao/RESULTADO_TESTES.md.

## 7. Limitações e trabalho futuro

Prioridade estrita pode prolongar espera de normais. Não há promoção automática, autosave, concorrência, múltiplos guichês ou autenticação. A renderização completa após cada alteração é adequada à demonstração acadêmica, sem promessa para grandes volumes.

## 8. Referência e conclusão

O projeto C/GTK de controle de pousos de George Mendes Marra inspirou organização, compartilhamento de núcleo e reclassificação reversível. A solução estende o sistema bancário Python existente e liga cada entregável a uma aplicação de desktop funcional.
