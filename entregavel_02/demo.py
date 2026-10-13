from contas import Conta,BancoEstatico,BancoDinamico
for tipo in (lambda:BancoEstatico(3),BancoDinamico):
 banco=tipo();conta=Conta('001','Ana',100);banco.inserir(conta)
 conta.depositar(50);conta.sacar(20)
 print(type(banco).__name__,banco.buscar('001').saldo,banco.quantidade())
