# 2 — TAD Conta Bancária

## Objetivo
Encapsulamento, capacidade fixa e objetos dinâmicos

## Implementação e interface
Conta encapsula saldo com métodos depositar e sacar. BancoEstatico usa vetor de capacidade fixa e deslocamento na remoção. BancoDinamico usa nós ligados e criação sob demanda. Interface pública: inserir, buscar, remover e quantidade, além dos métodos da conta.

## Execução
Na raiz, execute `python entregavel_02/demo.py`. Dentro desta pasta, use `python demo.py`.

## Testes
`python -m unittest discover -s . -p "testes*.py" -v`

## Complexidade
BancoEstatico: inserir O(n) devido à checagem de duplicidade; buscar O(n); remover O(n). BancoDinamico: inserir O(n) com checagem de duplicidade; buscar O(n); remover O(n). Armazenamento O(n) em ambas.

## Limitações e decisões
Em Python, o vetor é uma lista prealocada com tamanho fixo lógico, não uma alocação estática real de C. Os nós são objetos criados dinamicamente e liberados pelo coletor de lixo.


## Validação ampliada

9 testes nesta entrega, incluindo os originais e casos de fronteira em `testes_limites.py`. Na raiz: `python -m unittest discover -s entregavel_02 -p "testes*.py" -v`.

O TAD Conta usa `Decimal` para centavos exatos. Aceita valores finitos, não negativos e com até duas casas decimais; depósito/saque exige valor positivo. O saldo é exposto como Decimal. O exercício permanece independente do atendimento bancário.
