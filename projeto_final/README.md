# Projeto final — Sistema de Gerenciamento de Atendimento Bancário

Integra fila de prioridade, lista de histórico e duas pilhas de comandos. Oferece interface gráfica Tkinter e terminal usando o mesmo núcleo.

## Executar da raiz

```bash
python projeto_final/interface_grafica.py
python projeto_final/interface_grafica.py --demo
python projeto_final/main.py
python projeto_final/main.py --gui
```

Sem bibliotecas Python externas. Python 3.10+; Tkinter e display gráfico apenas para a GUI. Os atalhos `abrir_interface.bat` e `abrir_interface.sh` ficam na raiz.

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `cliente.py` | Registro imutável de cliente, senha, categoria e ordem de chegada |
| `estruturas.py` | Fila, pilha e lista encadeadas implementadas manualmente |
| `sistema.py` | Prioridade, cadastro, atendimento, pesquisa, cancelamento, undo/redo |
| `persistencia.py` | Sessões JSON validadas e exportação CSV |
| `main.py` | Interface de terminal |
| `interface_grafica.py` | Janela, tabelas, botões, indicadores e modo didático |
| `testes.py` | Dez testes originais |
| `testes_novos.py` | 36 testes adicionais de integração e persistência |
| `test_interface_grafica.py` | 15 testes de widgets reais, executados separadamente |
| `ESPECIFICACAO_TAD.md` | Contratos e invariantes |

## Testes

```bash
# Na raiz
python -m unittest discover -s projeto_final -p "testes*.py" -v
python executar_testes.py --gui
```

Dentro desta pasta, execute `python -m unittest test_interface_grafica -v` para testar somente a GUI.

## Regras

Prioridade estrita, FIFO por chegada em cada categoria; senha permanente mesmo após reclassificação. Atendimento e reclassificação são reversíveis; cadastro e cancelamento reiniciam as pilhas. Abrir sessão restaura dados e limpa reversões. Não há salvamento automático.

Veja [manual](../documentacao/MANUAL_USUARIO.md), [arquitetura](../documentacao/ARQUITETURA.md) e [relatório](RELATORIO.md).
