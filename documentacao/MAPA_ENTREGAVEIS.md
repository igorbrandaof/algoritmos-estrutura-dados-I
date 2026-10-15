# Mapa dos cinco entregáveis

| Entrega | Conteúdo preservado | Relação com projeto final | Testes |
|---|---|---|---:|
| 01 | Utilitários, parâmetros, fatorial/Fibonacci e busca binária recursiva | Modularização: domínio, persistência, terminal e GUI separados | 13 |
| 02 | Conta e bancos com armazenamento fixo/dinâmico | Contratos do TAD; validação e encapsulamento; Decimal no exercício monetário | 9 |
| 03 | Lista sequencial, simples, dupla e circular | Lista simplesmente encadeada no histórico | 9 |
| 04 | Pilha em array/encadeada e delimitadores balanceados | Duas pilhas encadeadas de comandos para undo/redo | 7 |
| 05 | Filas circular, encadeada e prioritária | Duas filas FIFO e prioridade estrita | 8 |
| Final | Atendimento bancário em Python | Integração, persistência e duas interfaces | 46 + 15 GUI |

Todos os entregáveis continuam autocontidos e executáveis por seus próprios arquivos `demo.py` e testes. Não se exige Tkinter para executar os cinco módulos.

## Validar um módulo

Na raiz, substitua 01 pelo módulo desejado:

```bash
python entregavel_01/demo.py
python -m unittest discover -s entregavel_01 -p "testes*.py" -v
```

## Diferenças entre Python e C

Python passa referências a objetos por atribuição; mutabilidade determina se uma função altera o objeto recebido. A alocação e liberação são gerenciadas pelo runtime. Listas prealocadas simulam capacidade fixa; não equivalem a memória estática de C. Por isso os testes verificam invariantes, limites e comportamento, sem alegar uso de malloc/free ou validação Valgrind do código Python.
