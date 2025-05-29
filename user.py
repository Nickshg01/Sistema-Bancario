from sys import exit
from pathlib import Path
from datetime import datetime
import json

if __name__ == '__main__':
    print('Este módulo não deve ser executado diretamente. ')
    exit()

from utils import ask, money_format, validate_num, update_data
import auth

class DigitalAccount():
    def __init__(self: object, **kwargs):
       self.name = kwargs['name']
       self.balance = kwargs['balance']
       self.statement = kwargs['statement']
       print(f'Seja bem vindo(a), {self.name.split()[0]}!\n')

    def view_balance(self: object) -> None:
        """Exibe o saldo do usuário na tela."""
        print(f'Saldo: {money_format(self.balance)}\n')

    def view_statement(self: object) -> None:
        """Exibe o extrato bancário do usuário na tela."""
        for operation in self.statement:
            for key, value in operation.items():
                print(f'{key}: {value}')
            print()

    def statement_append(self: object, transation: str, value: float, destiny: dict = None) -> dict:
        """Adiciona uma operação ao extrato bancário do usuário. 
        Caso a operação envolva um segundo usuário, o método retorna um dicionário com as informações do usuário
        após atualizar o extrato."""
        statement = {'Tipo': transation, 
                     'Valor': money_format(value)}
        
        if destiny is not None:
            statement['Origem'], statement['Destinatário'] = self.name, destiny['name']
        statement['Data'] = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.statement.append(statement)

        if destiny is not None:
            destiny['statement'].append(statement)
            return destiny

    def deposit(self: object, database: Path, cpf: str) -> None:
        """Adiciona um valor ao saldo do usuário."""
        value = validate_num('Quanto você deseja depositar? R$')
        if value <= 0:
            print(f'Não é possível fazer depósitos menores que {money_format(0)}.\n')
            return
        
        self.balance += value
        self.statement_append('Depósito', value)
        update_data(database, cpf, **self.__dict__)
        print(f'Depósito de {money_format(value)} realizado com sucesso! \n')

    def withdrawal(self: object, database: Path, cpf: str) -> None:
        """Retira um valor do saldo do usuário caso ele tenha tal valor na conta."""
        value = validate_num('Quanto você deseja sacar? R$')
        if value <= 0:
            print(f'Não é possível fazer saques com valores menores do que {money_format(0)}.\n')
            return 
        
        if value > self.balance:
            print('Saldo insuficiente. Nenhuma operação foi realizada.\n')
            return
        
        self.balance -= value
        self.statement_append('Saque', value)
        update_data(database, cpf, **self.__dict__)
        print(f'Saque de {money_format(value)} realizado com sucesso!\n')

    def transfer(self: object, database, cpf) -> None:
        """Manda um valor do saldo do usuário à outra conta, desde que o usuário tenha tal valor disponível."""
        while True:
            try:
                cpf_destiny = ask('Digite o CPF do destinatário: ').replace('.', '').replace('-', '')
                auth.auth_cpf(cpf_destiny)
                break

            except auth.InvalidCpfError:
                print('O CPF que você digitou é inválido. Verifique se escreveu corretamente. \n')
        
        if not auth.cpf_find(database, cpf_destiny):
            print('CPF não encontrado. \n')
            return
        
        with open(database, 'r', encoding='utf8') as file:
            destiny = json.load(file)[cpf_destiny]

        print(f'Nome: {destiny['name']}\nCPF: {cpf_destiny}\n')
        value = validate_num('Quanto você deseja transferir? R$')

        if value <= 0:
            print(f'Não é possível fazer transferências com valores menores que {money_format(0)}.\n')

        if value > self.balance:
            print('Saldo insuficiente. Nenhuma operação foi feita. \n')
            return
        
        self.balance -= value
        destiny['balance'] += value
        destiny = self.statement_append('Transferência', value, destiny)
        update_data(database, cpf, **self.__dict__)
        update_data(database, cpf_destiny, **destiny)

        print(f'Transferência de {money_format(value)} realizada com sucesso!\n')

    def income(self):
        """Faz o rendimento diário da conta digital."""
        pass


def create_object(database: Path, cpf: str) -> DigitalAccount:
    with open(database, 'r', encoding='utf8') as file:
        user_data = json.load(file)[cpf]

    return DigitalAccount(**user_data)
        
def main(database: Path, cpf: str) -> None:
    """Código principal do módulo user."""

    user = create_object(database, cpf)
    
    while True:
        option = ask('O que deseja fazer?\n[1]Mostrar saldo |[2]Depositar |[3]Sacar '
        '|[4]Checar extrato |[5]Transferir |[6]Sair\n\t')
        OPTIONS = {'1': lambda: user.view_balance(),
                   '2': lambda: user.deposit(database, cpf),
                   '3': lambda: user.withdrawal(database, cpf),
                   '4': lambda: user.view_statement(),
                   '5': lambda: user.transfer(database, cpf)}
        
        if option == '6':
            print('Você saiu da sua conta. \n')
            return
        
        executar = OPTIONS.get(option)
        executar() if executar else print('Opção inválida.')
