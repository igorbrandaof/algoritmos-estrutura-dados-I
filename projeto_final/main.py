from sistema import SistemaBancario

def imprimir_clientes(clientes):
 if not clientes:print('  Nenhum cliente.')
 for cliente in clientes:print(' ',cliente)

def executar():
 banco=SistemaBancario()
 while True:
  print('\n=== ATENDIMENTO BANCARIO ===')
  print('1 Cadastrar | 2 Atender | 3 Filas | 4 Historico')
  print('5 Desfazer ultimo atendimento | 6 Buscar atendido | 0 Sair')
  opcao=input('Opcao: ').strip()
  if opcao=='1':
   nome=input('Nome: ')
   tipo=input('Prioritario? (s/n): ').strip().lower()
   if tipo not in ('s','n'):
    print('Responda s ou n.');continue
   try:print('Cadastrado:',banco.cadastrar(nome,tipo=='s'))
   except ValueError as erro:print('Erro:',erro)
  elif opcao=='2':print('Atendido:',banco.atender() or 'Fila vazia')
  elif opcao=='3':
   prioridade,normal=banco.filas()
   print('PRIORITARIOS:');imprimir_clientes(prioridade)
   print('NORMAIS:');imprimir_clientes(normal)
  elif opcao=='4':print('HISTORICO (mais recente primeiro):');imprimir_clientes(banco.atendidos())
  elif opcao=='5':print('Desfeito:',banco.desfazer_ultimo() or 'Nenhum atendimento reversivel')
  elif opcao=='6':
   senha=input('Senha: ').strip().upper()
   print('Resultado:',banco.consultar_atendimento(senha) or 'Nao encontrada')
  elif opcao=='0':print('Ate logo!');break
  else:print('Opcao invalida')
if __name__=='__main__':executar()
