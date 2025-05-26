from sys import exit

if __name__ == '__main__':
    print('Este módulo não deve ser executado diretamente.')
    exit()

import json
from pathlib import Path

import auth, user
from utils import ask

def signup(database):
    """Cadastra um novo usuário no banco de dados."""

    name = ask('Digite seu nome: ')

    while True:
        try:
            cpf = ask('Digite seu CPF: ').replace('.', '').replace('-', '')
            auth.auth_cpf(cpf)
            
            if auth.cpf_find(database, cpf):
                print('O CPF digitado já está cadastrado. \n')
                return
            break

        except auth.InvalidCpfError:
            print('O CPF digitado é inválido. Digite novamente. \n')

        except FileNotFoundError:
            break

    user = {'name': name,
            'balance': 0.0,
            'statement': []}
    
    password = auth.create_password()
    user['password'], user['salt'] = auth.hash_password(password)

    try:
        users = {}
        with open(database, 'r', encoding='utf8') as file:
            users = json.load(file)

    except FileNotFoundError:
        print('Criando um novo banco de dados...')
    
    finally:
        with open(database, 'w', encoding='utf8') as file:
            users[cpf] = user
            json.dump(users, file, indent=4, ensure_ascii=False)
    print('Parabéns! Usuário cadastrado com sucesso! \n')


def login(database: Path) -> None:
    """Acessa a conta do usuário no banco de dados."""

    if not database.exists():
        raise FileNotFoundError

    while True:
        try:
            cpf = ask('Digite seu CPF: ').replace('.', '').replace('-', '')
            auth.auth_cpf(cpf)

            with open(database, 'r', encoding='utf8') as data:
                _ = json.load(data)
                user_data = _[cpf]
            break

        except auth.InvalidCpfError:
            print('O CPF que você digitou não é válido. Tente novamente. \n')
        
        except KeyError:
            print('CPF não encontrado.\n')
            return
        
    password = ask('Digite sua senha: ')

    if not auth.auth_password(password, user_data):
        raise PermissionError
    
    user.main(database, cpf)
