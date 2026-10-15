# Resultado de validação — versão com interface gráfica

Data: 14/10/2026 21:08 -03 · Python 3.12.14 · Linux.

Comando padrão: `python executar_testes.py` (92 testes).  
Comando com GUI: `python executar_testes.py --gui` (107 testes).

A execução da GUI utilizou display virtual Xvfb e widgets Tkinter reais. Os diálogos modais são simulados nos testes para verificar decisões sem intervenção manual. A janela foi também renderizada e inspecionada em 1240×820 e 1060×740; capturas foram incluídas na documentação.

| Suíte | Aprovados |
|---|---:|
| Entregável 01 | 13 |
| Entregável 02 | 9 |
| Entregável 03 | 9 |
| Entregável 04 | 7 |
| Entregável 05 | 8 |
| Projeto final: domínio/persistência | 46 |
| Interface gráfica | 15 |
| **Total** | **107** |

Os 28 testes originais foram preservados. As cinco demonstrações executaram sem erro. O terminal foi exercitado com cadastro normal/prioritário, atendimento, desfazer, refazer e indicadores. Os links locais Markdown e a compilação sintática dos arquivos Python foram conferidos.

Limites: não houve execução nativa no Windows/macOS nem do workflow remoto. Não se alega cobertura de linhas medida ou validação para uso bancário real. As versões Python da matriz CI ainda serão verificadas após envio aprovado.

## Saída completa

```text

============================================================
entregavel_01
test_busca (testes.TesteUtilitarios.test_busca) ... ok
test_fatorial (testes.TesteUtilitarios.test_fatorial) ... ok
test_fibonacci (testes.TesteUtilitarios.test_fibonacci) ... ok
test_invalido (testes.TesteUtilitarios.test_invalido) ... ok
test_media (testes.TesteUtilitarios.test_media) ... ok
test_mutacao (testes.TesteUtilitarios.test_mutacao) ... ok
test_troca (testes.TesteUtilitarios.test_troca) ... ok
test_busca_duplicatas (testes_limites.TestesLimites.test_busca_duplicatas) ... ok
test_busca_vazia_extremidades_ausente (testes_limites.TestesLimites.test_busca_vazia_extremidades_ausente) ... ok
test_media_vazia_e_negativos (testes_limites.TestesLimites.test_media_vazia_e_negativos) ... ok
test_recursao_bases (testes_limites.TestesLimites.test_recursao_bases) ... ok
test_referencias_mutaveis_e_imutaveis (testes_limites.TestesLimites.test_referencias_mutaveis_e_imutaveis) ... ok
test_tipos_invalidos (testes_limites.TestesLimites.test_tipos_invalidos) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.000s

OK

============================================================
entregavel_02
test_capacidade (testes.Testes.test_capacidade) ... ok
test_implementacoes (testes.Testes.test_implementacoes) ... ok
test_saldo (testes.Testes.test_saldo) ... ok
test_capacidade_invalida (testes_limites.TestesLimites.test_capacidade_invalida) ... ok
test_centavos_exatos (testes_limites.TestesLimites.test_centavos_exatos) ... ok
test_dados_invalidos (testes_limites.TestesLimites.test_dados_invalidos) ... ok
test_duplicata_em_ambos_tads (testes_limites.TestesLimites.test_duplicata_em_ambos_tads) ... ok
test_remover_inicio_meio_fim_e_reutilizar (testes_limites.TestesLimites.test_remover_inicio_meio_fim_e_reutilizar) ... ok
test_valores_invalidos_nao_alteram_saldo (testes_limites.TestesLimites.test_valores_invalidos_nao_alteram_saldo) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK

============================================================
entregavel_03
test_circular (testes.Testes.test_circular) ... ok
test_dupla (testes.Testes.test_dupla) ... ok
test_listas (testes.Testes.test_listas) ... ok
test_busca_ausente (testes_limites.TestesLimites.test_busca_ausente) ... ok
test_capacidade_e_reaproveitamento (testes_limites.TestesLimites.test_capacidade_e_reaproveitamento) ... ok
test_circular_ciclo_e_reutilizacao (testes_limites.TestesLimites.test_circular_ciclo_e_reutilizacao) ... ok
test_dupla_referencias_apos_esvaziar (testes_limites.TestesLimites.test_dupla_referencias_apos_esvaziar) ... ok
test_insercao_remocao_meio (testes_limites.TestesLimites.test_insercao_remocao_meio) ... ok
test_limites_de_indice (testes_limites.TestesLimites.test_limites_de_indice) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK

============================================================
entregavel_04
test_balanceamento (testes.Testes.test_balanceamento) ... ok
test_pilhas (testes.Testes.test_pilhas) ... ok
test_balanceados_com_texto (testes_limites.TestesLimites.test_balanceados_com_texto) ... ok
test_balanceamento_falhas (testes_limites.TestesLimites.test_balanceamento_falhas) ... ok
test_capacidade_invalida (testes_limites.TestesLimites.test_capacidade_invalida) ... ok
test_lifo_ambas_representacoes (testes_limites.TestesLimites.test_lifo_ambas_representacoes) ... ok
test_overflow_e_reutilizacao (testes_limites.TestesLimites.test_overflow_e_reutilizacao) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK

============================================================
entregavel_05
test_circular_wrap (testes.Testes.test_circular_wrap) ... ok
test_filas (testes.Testes.test_filas) ... ok
test_prioridade (testes.Testes.test_prioridade) ... ok
test_capacidade_invalida (testes_limites.TestesLimites.test_capacidade_invalida) ... ok
test_circular_varias_voltas (testes_limites.TestesLimites.test_circular_varias_voltas) ... ok
test_fifo_ambas_representacoes (testes_limites.TestesLimites.test_fifo_ambas_representacoes) ... ok
test_overflow_nao_perde_elementos (testes_limites.TestesLimites.test_overflow_nao_perde_elementos) ... ok
test_prioridade_e_fifo_em_cada_categoria (testes_limites.TestesLimites.test_prioridade_e_fifo_em_cada_categoria) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.000s

OK

============================================================
projeto_final
test_fila (testes.TesteEstruturas.test_fila) ... ok
test_lista (testes.TesteEstruturas.test_lista) ... ok
test_pilha (testes.TesteEstruturas.test_pilha) ... ok
test_busca (testes.TesteSistema.test_busca) ... ok
test_cadastro_invalida_desfazer (testes.TesteSistema.test_cadastro_invalida_desfazer) ... ok
test_desfazer_sequencia (testes.TesteSistema.test_desfazer_sequencia) ... ok
test_nome_invalido (testes.TesteSistema.test_nome_invalido) ... ok
test_prioridade_e_fifo (testes.TesteSistema.test_prioridade_e_fifo) ... ok
test_senhas (testes.TesteSistema.test_senhas) ... ok
test_vazio (testes.TesteSistema.test_vazio) ... ok
test_cadastro_invalida_ambas_pilhas (testes_novos.TesteOperacoes.test_cadastro_invalida_ambas_pilhas) ... ok
test_cancelar_inexistente_nao_muda_pilhas (testes_novos.TesteOperacoes.test_cancelar_inexistente_nao_muda_pilhas) ... ok
test_cancelar_limpa_reversoes_e_mantem_historico (testes_novos.TesteOperacoes.test_cancelar_limpa_reversoes_e_mantem_historico) ... ok
test_categoria_invalida_rejeita (testes_novos.TesteOperacoes.test_categoria_invalida_rejeita) ... ok
test_estatisticas_totais (testes_novos.TesteOperacoes.test_estatisticas_totais) ... ok
test_esvaziar_e_reutilizar_fila (testes_novos.TesteOperacoes.test_esvaziar_e_reutilizar_fila) ... ok
test_fluxo_longo_desfazer_refazer (testes_novos.TesteOperacoes.test_fluxo_longo_desfazer_refazer) ... ok
test_nome_longo_nao_consume_senha (testes_novos.TesteOperacoes.test_nome_longo_nao_consume_senha) ... ok
test_normalizar_nome (testes_novos.TesteOperacoes.test_normalizar_nome) ... ok
test_nova_operacao_invalida_refazer (testes_novos.TesteOperacoes.test_nova_operacao_invalida_refazer) ... ok
test_operacoes_intercaladas (testes_novos.TesteOperacoes.test_operacoes_intercaladas) ... ok
test_pesquisa_nome_senha_sem_sensibilidade_caixa (testes_novos.TesteOperacoes.test_pesquisa_nome_senha_sem_sensibilidade_caixa) ... ok
test_prioridade_consistente_com_proximo (testes_novos.TesteOperacoes.test_prioridade_consistente_com_proximo) ... ok
test_reclassificar_atendido_rejeita (testes_novos.TesteOperacoes.test_reclassificar_atendido_rejeita) ... ok
test_reclassificar_categoria_igual_nao_invalida_pilhas (testes_novos.TesteOperacoes.test_reclassificar_categoria_igual_nao_invalida_pilhas) ... ok
test_reclassificar_desfazer_refazer (testes_novos.TesteOperacoes.test_reclassificar_desfazer_refazer) ... ok
test_reclassificar_preserva_chegada_e_senha (testes_novos.TesteOperacoes.test_reclassificar_preserva_chegada_e_senha) ... ok
test_refazer_atendimento (testes_novos.TesteOperacoes.test_refazer_atendimento) ... ok
test_remover_fim_e_inserir_novamente (testes_novos.TesteOperacoes.test_remover_fim_e_inserir_novamente) ... ok
test_cliente_duplicado (testes_novos.TestePersistencia.test_cliente_duplicado) ... ok
test_contador_booleano (testes_novos.TestePersistencia.test_contador_booleano) ... ok
test_csv_formula_nao_e_executavel (testes_novos.TestePersistencia.test_csv_formula_nao_e_executavel) ... ok
test_csv_nome_com_delimitador_e_unicode (testes_novos.TestePersistencia.test_csv_nome_com_delimitador_e_unicode) ... ok
test_fila_incorreta (testes_novos.TestePersistencia.test_fila_incorreta) ... ok
test_json_corrompido (testes_novos.TestePersistencia.test_json_corrompido) ... ok
test_limite_tamanho (testes_novos.TestePersistencia.test_limite_tamanho) ... ok
test_ordem_duplicada (testes_novos.TestePersistencia.test_ordem_duplicada) ... ok
test_ordem_fifo_invertida (testes_novos.TestePersistencia.test_ordem_fifo_invertida) ... ok
test_prioridade_string (testes_novos.TestePersistencia.test_prioridade_string) ... ok
test_roundtrip_e_contadores (testes_novos.TestePersistencia.test_roundtrip_e_contadores) ... ok
test_roundtrip_reclassificacao_cancelamento (testes_novos.TestePersistencia.test_roundtrip_reclassificacao_cancelamento) ... ok
test_salvamento_atomico_em_falha (testes_novos.TestePersistencia.test_salvamento_atomico_em_falha) ... ok
test_senha_invalida (testes_novos.TestePersistencia.test_senha_invalida) ... ok
test_sessao_vazia (testes_novos.TestePersistencia.test_sessao_vazia) ... ok
test_totais_inconsistentes (testes_novos.TestePersistencia.test_totais_inconsistentes) ... ok
test_versao_invalida (testes_novos.TestePersistencia.test_versao_invalida) ... ok

----------------------------------------------------------------------
Ran 46 tests in 0.015s

OK

Resultado: 6/6 suítes aprovadas
test_abas_e_layout_minimo (test_interface_grafica.TesteInterface.test_abas_e_layout_minimo) ... ok
test_abrir_corrompido_preserva_sessao (test_interface_grafica.TesteInterface.test_abrir_corrompido_preserva_sessao) ... ok
test_atender_desfazer_refazer_atualiza_historico (test_interface_grafica.TesteInterface.test_atender_desfazer_refazer_atualiza_historico) ... ok
test_busca_nao_muda_ordem_atendimento (test_interface_grafica.TesteInterface.test_busca_nao_muda_ordem_atendimento) ... ok
test_cadastro_invalido_mostra_erro (test_interface_grafica.TesteInterface.test_cadastro_invalido_mostra_erro) ... ok
test_cadastro_tabela_e_indicador (test_interface_grafica.TesteInterface.test_cadastro_tabela_e_indicador) ... ok
test_cancelamento_confirmado (test_interface_grafica.TesteInterface.test_cancelamento_confirmado) ... ok
test_cancelamento_recusado_preserva_fila (test_interface_grafica.TesteInterface.test_cancelamento_recusado_preserva_fila) ... ok
test_cancelar_dialogo_salvar_mantem_alterado (test_interface_grafica.TesteInterface.test_cancelar_dialogo_salvar_mantem_alterado) ... ok
test_exportar_csv_nao_marca_sessao_salva (test_interface_grafica.TesteInterface.test_exportar_csv_nao_marca_sessao_salva) ... ok
test_inicio_vazio_botoes_desabilitados (test_interface_grafica.TesteInterface.test_inicio_vazio_botoes_desabilitados) ... ok
test_prioritario_primeiro (test_interface_grafica.TesteInterface.test_prioritario_primeiro) ... ok
test_protecao_contra_perda_cancelar (test_interface_grafica.TesteInterface.test_protecao_contra_perda_cancelar) ... ok
test_reclassificacao_com_confirmacao (test_interface_grafica.TesteInterface.test_reclassificacao_com_confirmacao) ... ok
test_salvar_e_abrir_sessao (test_interface_grafica.TesteInterface.test_salvar_e_abrir_sessao) ... ok

----------------------------------------------------------------------
Ran 15 tests in 2.250s

OK
```
