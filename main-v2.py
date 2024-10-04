"""
REGRAS DO SISTEMAS

Para a primeira versao do sistema, devemos implementar apenas 3 operaçoes: deposito, saque e extrato.
O sistema terá apenas 1 usuario e nao deve permitir valores negativos.

DEPOSITO:
    - Todos os depositos devem ser armazenados em uma variavel e exibidos na operaçao de extrato.

SAQUE:
    - O sistema deve permitir 3 saques diarios com limite maximo de R$500 por saque;
    - Se nao houver saldo em conta, exibir uma mensagem informando que nao sera possivel sacar por falta de saldo;
    - Todos os saques devem ser armazenados em uma variavel e exibidos na operaçao de extrato.

EXTRATO:
    - Esta operaçao deve listar todos os depositos e saques realizados na conta e no fim deve exibir o saldo atual;
    - Os valores devem ser exibidos no formato R$xxx.xx (R$1500.45)

Com os novos conhecimentos adquiridos sobre data e hora, você foi encarregado de implementar as seguintes funcionalidades 
no sistema:
    - Estabelecer um limite de 10 transações diárias para uma conta;
    - Se o usuário tentar fazer uma transação após atingir o limite, deve ser informado que ele excedeu o número de 
      transações permitidas para aquele dia;
    - Mostre no extrato, a data e hora de todas as transações.

DESAFIO
Precisamos deixar o nosso codigo modularizado. Crie funçoes para as operaçoes existentes: 
    - deposito, saque e extrato.
E crie duas novas funçoes: 
    - criar_usuario (cliente do banco) e criar_conta_corrente (vincular com usuario).
Novas restriçoes para a v2 do sistema bancario:
    - A funçao SAQUE() deve receber os argumentos apenas por nome (keyword only). 
      Sugestao de argumentos:
        - saldo, valor, extrato, limite, numero_saques, limite_saques.
      Sugestao de retorno: 
        - saldo e extrato.
    - A funçao DEPOSITO() deve receber os argumentos apenas por posiçao (positional only). 
      Sugestao de argumentos: 
        - - saldo, valor, extrato. 
      Sugestao de retorno: 
        - - saldo e extrato.
    - A funçao EXTRATO() deve receber os argumentos por posiçao e nome (positional only e keyword only). 
      Argumentos posicionais: 
        - saldo 
      Argumentos nomeados: 
        - extrato.
    - Na funçao CRIAR_USUARIO() o programa deve armazenar os usuarios em uma lista. 
      Um usuarios é composto por: 
        - nome, data de nascimento, cpf e endereço. Um usuarios deve ter: - nome, data de nascimento, cpf e endereço. 
      O endereço é uma string com o formato: 
        - logradouro, nro - bairro - cidade/sigla estado. 
      Deve ser armazenado somente os numeros do CPF. Nao podemos cadastrar 2 usuarios com o mesmo CPF.
    - Na funçao CRIAR_CONTA_CORRENTE() o programa deve armazenar as contas correntes em uma lista. 
      Uma conta é composta por: 
        - agencia, numero da conta e usuario. 
      O numero da conta é sequencial, iniciando em 1. O numero da agencia é fixo: "0001". 
      O usuario pode ter mais de uma conta, mas uma conta pertence a somente um usuario.
    DICA
    - Para vincular um usuario a uma conta, filtre a lista de usuarios buscando o numero do CPF informado para cada 
      usuario da lista.

"""

from datetime import datetime


def menu():
    menu = """
===================== SISTEMA BANCARIO =====================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuario
    [lu] Listar Usuarios
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    return input(menu)


def depositar(saldo, quantia, extrato, /):
    if quantia > 0:
        saldo += quantia
        print(f"Seu deposito de R${quantia:.2f} foi efetuado!")
        gravar_transacao("d", quantia, extrato)
    else:
        print("O valor é inválido! Tente novamente.")
    return saldo


def sacar(*, saldo, quantia, numero_saques, limite_por_saque, LIMITE_SAQUES, extrato):
    regra_saldo = saldo >= quantia
    regra_limite = limite_por_saque >= quantia
    regra_saque = numero_saques < LIMITE_SAQUES
    if quantia > 0:
        if not regra_saldo:
            print("Voce nao tem saldo para realizar esta operaçao. Confira no extrato e tente novamente.")
        elif not regra_limite:
            print("Voce nao tem limite para realizar esta operaçao. Confira no extrato e tente novamente.")
        elif not regra_saque:
            print("Voce nao tem saque disponivel para realizar esta operaçao. Confira no extrato e tente novamente.")
        else:
            saldo -= quantia
            numero_saques += 1
            print(f"Seu saque de R${quantia:.2f} foi efetuado!")
            gravar_transacao("s", quantia, extrato)
    else:
        print("A operação não é válida! Tente novamente.")
    return saldo, numero_saques


def extrato_completo(saldo, /, *, extrato, numero_saques, LIMITE_SAQUES):
    qtd_saques = LIMITE_SAQUES - numero_saques
    cabecalhos = ["Data", "Tipo", "Valor"]

    print("===================  EXTRATO ========================")
    print(f"Seu saldo é de R${saldo:.2f}.")
    print(f"Voce tem {qtd_saques} saque(s).")
    print("=================== HISTORICO =======================")

    if extrato:
        print(f"{cabecalhos[0].center(20)} | {cabecalhos[1].center(10)} | {cabecalhos[2].center(10)}")
        for reg in extrato:
            print(f"{reg[0].center(20)} | {reg[1].center(10)} | {reg[2]}")
    else:
        print("Nao houveram movimentaçoes.")


def gravar_transacao(opcao, quantia, extrato):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    if quantia > 0:
        if opcao == "d":
            extrato.append([data, "Deposito", quantia])
        elif opcao == "s":
            extrato.append([data, "Saque", quantia])
    else:
        print("Transação inválida! Tente novamente.")


def filtrar_usuarios(cpf, usuarios):
    usuario_filtrado = [usuario for i, usuario in enumerate(usuarios) if usuarios[i]['cpf'] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None


def criar_usuario(cpf, usuarios):
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("Usuário já existe")
    nome = input("Nome: ")
    if nome:
        data_nascimento = input("Data de nascimento: ")
        endereco = input("Endereço: (logradouro, nro - bairro - cidade/sigla estado): ")
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        print("=========================== Usuário criado com sucesso! ===========================")
    else:
        print("Digite um nome para o titular valido!")


def listar_usuarios(usuarios):
    print(" ====================== USUARIOS ======================")
    if usuarios:
        for cc, usuario in enumerate(usuarios):
            saida = f"""
    CPF: {usuarios[cc]['cpf']} | Titular: {usuarios[cc]['nome']} | Nascimento: {usuarios[cc]['data_nascimento']} | Endereço: {usuarios[cc]['endereco']}
            """
            print(saida)
    else:
        print("Nao existem usuarios cadastrados!")


def criar_conta_corrente(cpf, agencia, numero_conta, contas, usuarios):
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print("======================== Conta criada com sucesso! ========================")
    else:
        print("======================== Usuário não encontrado! ========================")


def listar_contas(contas):
    print(" ======================= CONTAS =======================")
    if contas:
        for i, conta in enumerate(contas):
            saida = f"""
    Agencia: {contas[i]['agencia']} | Conta Corrente: {contas[i]['numero_conta']} | CPF: {contas[i]['usuario']['cpf']} | Titular: {contas[i]['usuario']['nome']}
            """
            print(saida)
    else:
        print("Nao existem contas cadastradas!")


def main():

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite_por_saque = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        
        opcao = menu()

        if opcao == "d":
            try:
                quantia = float(input("Qual quantia deseja depositar? "))
                saldo = depositar(saldo, quantia, extrato)
            except Exception as e:
                print(f"Não foi possivel realizar o depósito! Erro: {e}")

        elif opcao == "s":
            try:
                quantia = float(input("Qual quantia deseja sacar? "))
                saldo, numero_saques = sacar(
                    saldo = saldo, 
                    quantia = quantia, 
                    numero_saques = numero_saques, 
                    limite_por_saque = limite_por_saque, 
                    LIMITE_SAQUES = LIMITE_SAQUES,
                    extrato = extrato
                )
            except Exception as e:
                print(f"Não foi possivel realizar o saque! Erro: {e}")

        elif opcao == "e":
            extrato_completo(
                saldo,
                extrato = extrato, 
                numero_saques = numero_saques, 
                LIMITE_SAQUES = LIMITE_SAQUES
            )

        elif opcao == "nu":
            cpf = input("Digite o CPF (somente números): ")
            if cpf.isdigit() and len(cpf) == 11:
                criar_usuario(cpf, usuarios)
            else:
                print("Digite um CPF valido!")

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "nc":
            cpf = input("Digite o CPF (somente números): ")
            if cpf.isdigit() and len(cpf) == 11:
                criar_conta_corrente(cpf, AGENCIA, numero_conta, contas, usuarios)
                numero_conta += 1
            else:
                print("Digite um CPF valido!")
    
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print('Opção inválida! Tente novamente.')


if __name__ == "__main__":
    main()
