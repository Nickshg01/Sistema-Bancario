from sys import exit
from pathlib import Path

if __name__ == '__main__':
    print('Este módulo não deve ser executado diretamente. ')
    exit()

import json
from utils import ask, money_format

class DigitalAccount():
    def __init__(self: object, **kwargs):
       self._user = kwargs['name']
       self._balance = kwargs['balance']
       self._statement = kwargs['statement']
       print(f'Bem vindo, {self._user}!\n')

    def view_balance(self: object) -> None:
        """Exibe o saldo do usuário na tela."""
        print(f'Saldo: {money_format(self._balance)}\n')

    def view_statement(self: object) -> None:
        """Exibe o extrato bancário do usuário na tela."""
        print(self._statement)

    def deposit(self: object) -> None:
        """Adiciona um valor ao saldo do usuário."""
        value = float(ask('Quanto você deseja depositar? '))

    def withdrawal(self: object) -> None:
        """Retira um valor do saldo do usuário."""
        value = ask('Quanto você deseja sacar? ')

    def transfer(self: object) -> None:
        """Manda um valor do saldo do usuário à outra conta."""
        destiny = ask('Digite o CPF do destinatário: ')

    def income(self):
        pass

    def logout(self: object) -> None:
        """Chama o método __del__."""
        del self

    def __del__(self: object) -> None:
        """Atualiza o banco de dados e deleta o objeto"""
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
                   '2': lambda: user.deposit(),
                   '3': lambda: user.withdrawal(),
                   '4': lambda: user.view_statement(),
                   '5': lambda: user.transfer(),
                   '6': lambda: user.logout()}
        
        executar = OPTIONS.get(option)
        executar() if executar else print('Opção inválida.')
