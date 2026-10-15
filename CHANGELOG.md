# Histórico de alterações

## Versão com interface gráfica — proposta de revisão

- Acrescenta interface desktop Tkinter/ttk, tabelas, indicadores, busca e aba didática.
- Mantém terminal e cinco entregáveis; GUI e CLI usam o mesmo núcleo.
- Acrescenta reclassificação estável, refazer, cancelamento e estatísticas.
- Acrescenta persistência JSON validada com salvamento atômico e relatório CSV.
- Amplia de 28 para 107 testes: 92 de núcleo/módulos e 15 de interface real.
- Fortalece validações de recursão/capacidade e usa Decimal no TAD Conta.
- Preenche identificação acadêmica dos relatórios individuais com os dados do README original.
- Acrescenta manuais, especificação do TAD, arquitetura, mapa da disciplina e capturas de tela.
- Acrescenta workflow GitHub Actions para testes do núcleo e GUI.
- Preserva a apresentação PowerPoint original e corrige a identificação acadêmica no relatório Word.
- Remove o checklist de entrega e o roteiro de apresentação conforme solicitado.

Mudanças comportamentais: senha passa a ser permanente após reclassificação; cadastro/cancelamento limpa ambas as pilhas; carregamento inicia reversões vazias; a interface pergunta sobre alterações não salvas.
