from pathlib import Path
from sys import exit as _exit

DATABASE = Path(__file__).parent / 'bank_data' / 'users.json'
DATABASE.parent.mkdir(parents=True, exist_ok=True)

import account
from utils import ask

def exit():
    print('Você saiu do programa. ')
    _exit()

def main():
    """Código principal do módulo main"""
    while True:
        option = ask('Digite uma opção: \n[1]Cadastrar |[2]Fazer login |[3]Sair\n\t')

        OPTIONS = {'1': lambda: account.signup(DATABASE),
                   '2': lambda: account.login(DATABASE),
                   '3': lambda: exit()}
        try:
            executar = OPTIONS.get(option)
            executar() if executar else print('Opção inválida.\n')
        
        except FileNotFoundError:
            print('Banco de dados não encontrado. Tente cadastrar um usuário primeiro. \n')
        
        except PermissionError:
            print('Senha incorreta.\n')

if __name__ == '__main__':
    main()
