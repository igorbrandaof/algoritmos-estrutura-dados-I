"""Sessões JSON validadas e exportação CSV; sem dependências externas."""
import csv
import json
import os
import re
import tempfile
from dataclasses import asdict
from pathlib import Path

if __package__:
    from .cliente import Cliente
    from .sistema import SistemaBancario
else:
    from cliente import Cliente
    from sistema import SistemaBancario

VERSAO = 1
LIMITE_ARQUIVO = 5 * 1024 * 1024


def salvar_sessao(sistema, caminho):
    """Escrita atômica: uma falha não substitui o arquivo anterior por JSON parcial."""
    dados = {
        "versao": VERSAO,
        "contadores": {"normal": sistema._seq_normal, "prioritaria": sistema._seq_prioritaria,
                       "ordem": sistema._ordem, "cancelados": sistema.cancelados},
        "normal": [asdict(c) for c in sistema.normal],
        "prioritaria": [asdict(c) for c in sistema.prioritaria],
        "historico": [asdict(c) for c in sistema.historico],
    }
    caminho = Path(caminho)
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=caminho.parent,
                                         prefix=".sessao-", suffix=".tmp", delete=False) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, caminho)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def _inteiro(valor):
    return type(valor) is int and valor >= 0


def carregar_sessao(caminho):
    """Cria um novo sistema somente após validar todo o documento.

    Pilhas de undo/redo são da sessão de execução e não são serializadas.
    """
    caminho = Path(caminho)
    if caminho.stat().st_size > LIMITE_ARQUIVO:
        raise ValueError("Arquivo de sessão maior que 5 MB.")
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, RecursionError) as erro:
        raise ValueError("Arquivo de sessão inválido.") from erro
    if not isinstance(dados, dict) or type(dados.get("versao")) is not int or dados["versao"] != VERSAO:
        raise ValueError("Versão de sessão não suportada.")
    contadores = dados.get("contadores")
    chaves = {"normal", "prioritaria", "ordem", "cancelados"}
    if not isinstance(contadores, dict) or set(contadores) != chaves or not all(_inteiro(v) for v in contadores.values()):
        raise ValueError("Contadores de sessão inválidos.")
    grupos, senhas, ordens = {}, set(), set()
    for grupo in ("normal", "prioritaria", "historico"):
        itens = dados.get(grupo)
        if not isinstance(itens, list):
            raise ValueError("Lista de clientes inválida.")
        grupos[grupo] = []
        for item in itens:
            if not isinstance(item, dict) or set(item) != {"nome", "senha", "prioritario", "ordem"}:
                raise ValueError("Registro de cliente inválido.")
            nome, senha, prioridade, ordem = (item[k] for k in ("nome", "senha", "prioritario", "ordem"))
            if not isinstance(nome, str) or not nome.strip() or len(nome) > 100 or nome != " ".join(nome.split()):
                raise ValueError("Nome de cliente inválido.")
            if not isinstance(senha, str) or not re.fullmatch(r"[NP][0-9]{3,}", senha):
                raise ValueError("Senha de cliente inválida.")
            numero = int(senha[1:])
            chave = "normal" if senha[0] == "N" else "prioritaria"
            if numero < 1 or numero > contadores[chave] or senha != f"{senha[0]}{numero:03d}":
                raise ValueError("Sequência de senhas inconsistente.")
            if type(prioridade) is not bool or not _inteiro(ordem) or ordem < 1 or ordem > contadores["ordem"]:
                raise ValueError("Prioridade ou ordem inválida.")
            if senha in senhas or ordem in ordens:
                raise ValueError("Cliente duplicado na sessão.")
            if grupo != "historico" and prioridade != (grupo == "prioritaria"):
                raise ValueError("Cliente na fila incorreta.")
            senhas.add(senha)
            ordens.add(ordem)
            grupos[grupo].append(Cliente(nome, senha, prioridade, ordem))
        if grupo != "historico" and any(a.ordem >= b.ordem for a, b in zip(grupos[grupo], grupos[grupo][1:])):
            raise ValueError("Ordem FIFO inconsistente.")
    total = contadores["normal"] + contadores["prioritaria"]
    if total != contadores["ordem"] or len(senhas) + contadores["cancelados"] != total:
        raise ValueError("Totais de sessão inconsistentes.")
    sistema = SistemaBancario()
    sistema._seq_normal = contadores["normal"]
    sistema._seq_prioritaria = contadores["prioritaria"]
    sistema._ordem = contadores["ordem"]
    sistema.cancelados = contadores["cancelados"]
    for c in grupos["normal"]:
        sistema.normal.enfileirar(c)
    for c in grupos["prioritaria"]:
        sistema.prioritaria.enfileirar(c)
    for c in reversed(grupos["historico"]):
        sistema.historico.inserir_inicio(c)
    return sistema


def _texto_csv(texto):
    # Evita interpretar nomes fornecidos pelo usuário como fórmulas em planilhas.
    return "'" + texto if texto.lstrip().startswith(("=", "+", "-", "@")) else texto


def exportar_csv(sistema, caminho):
    """Relatório de fila e histórico em UTF-8 com BOM, separado por ponto e vírgula."""
    with Path(caminho).open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(("Situacao", "Senha", "Nome", "Categoria", "Ordem de chegada"))
        for situacao, clientes in (("Em espera", sistema.fila_ordenada()), ("Atendido", sistema.atendidos())):
            for cliente in clientes:
                escritor.writerow((situacao, cliente.senha, _texto_csv(cliente.nome), cliente.categoria, cliente.ordem))
