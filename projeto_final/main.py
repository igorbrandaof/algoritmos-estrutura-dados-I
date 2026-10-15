"""Interface de terminal; compartilha as regras com a interface gráfica."""
import argparse

if __package__:
    from .sistema import SistemaBancario
    from .persistencia import salvar_sessao, carregar_sessao, exportar_csv
else:
    from sistema import SistemaBancario
    from persistencia import salvar_sessao, carregar_sessao, exportar_csv


def imprimir_clientes(clientes):
    if not clientes:
        print("  Nenhum cliente.")
    for cliente in clientes:
        print(" ", cliente)


def ler_prioridade():
    tipo = input("Prioritário? (s/n): ").strip().lower()
    if tipo not in ("s", "n"):
        raise ValueError("Responda s ou n.")
    return tipo == "s"


def executar():
    banco = SistemaBancario()
    while True:
        print("\n=== ATENDIMENTO BANCÁRIO ===")
        print("1 Cadastrar | 2 Atender | 3 Filas | 4 Histórico")
        print("5 Desfazer | 6 Buscar atendido | 7 Refazer | 8 Reclassificar")
        print("9 Cancelar | 10 Indicadores | 11 Salvar | 12 Abrir | 13 Exportar CSV | 0 Sair")
        opcao = input("Opção: ").strip()
        try:
            if opcao == "1":
                nome = input("Nome: ")
                print("Cadastrado:", banco.cadastrar(nome, ler_prioridade()))
            elif opcao == "2":
                print("Atendido:", banco.atender() or "Fila vazia")
            elif opcao == "3":
                imprimir_clientes(banco.fila_ordenada())
            elif opcao == "4":
                imprimir_clientes(banco.atendidos())
            elif opcao == "5":
                print("Desfeito:", banco.desfazer_ultimo() or "Nada para desfazer")
            elif opcao == "6":
                print("Resultado:", banco.consultar_atendimento(input("Senha: ")) or "Não encontrada")
            elif opcao == "7":
                print("Refeito:", banco.refazer_ultimo() or "Nada para refazer")
            elif opcao == "8":
                senha = input("Senha do cliente em espera: ")
                print("Reclassificado:", banco.reclassificar(senha, ler_prioridade()))
            elif opcao == "9":
                senha = input("Senha do cliente em espera: ")
                if input("Confirmar cancelamento? (s/n): ").strip().lower() == "s":
                    print("Cancelado:", banco.cancelar(senha) or "Não encontrado")
            elif opcao == "10":
                print(banco.estatisticas())
            elif opcao == "11":
                salvar_sessao(banco, input("Arquivo JSON de destino: ").strip())
                print("Sessão salva.")
            elif opcao == "12":
                caminho = input("Arquivo JSON: ").strip()
                novo = carregar_sessao(caminho)
                if input("Substituir sessão atual? (s/n): ").strip().lower() == "s":
                    banco = novo
                    print("Sessão aberta.")
            elif opcao == "13":
                exportar_csv(banco, input("Arquivo CSV de destino: ").strip())
                print("Relatório exportado.")
            elif opcao == "0":
                print("Até logo! Use Salvar para manter os dados entre execuções.")
                break
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as erro:
            print("Erro:", erro)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema acadêmico de atendimento bancário")
    parser.add_argument("--gui", action="store_true", help="abrir interface gráfica")
    args = parser.parse_args()
    if args.gui:
        if __package__:
            from .interface_grafica import executar as executar_gui
        else:
            from interface_grafica import executar as executar_gui
        executar_gui()
    else:
        try:
            executar()
        except (EOFError, KeyboardInterrupt):
            print("\nSessão encerrada.")
