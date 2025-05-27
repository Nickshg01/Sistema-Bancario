from sys import exit

if __name__ == '__main__':
    print('Este módulo não deve ser executado diretamente.')
    exit()

from hashlib import pbkdf2_hmac
from pathlib import Path
import json, string, os

from utils import ask
    

class InvalidCpfError (Exception): pass


def hash_password(password: str) -> str:
    """Cria uma versão criptografada da senha e adiciona aos dados do usuário."""

    salt = os.urandom(16)
    hash = pbkdf2_hmac('SHA256', password.encode(), salt, 500_000)
    return hash.hex(), salt.hex()


def auth_password(password: str, user: dict) -> bool:
    """Compara o hash da senha digitada pelo usuário com o hash da senha armazenada no banco de dados."""

    hash, salt = user['password'], bytes.fromhex(user['salt'])
    password = pbkdf2_hmac('SHA256', password.encode(), salt, 500_000).hex()

    if password == hash:
        return True
    return False

def create_password() -> str:
    """
    Solicita que o usuário digite uma senha forte, verificando se ela atende aos
    requisitos:
    Pelo menos 8 caracteres;
    Pelo menos um número;
    Pelo menos 1 caractere maiúsculo;
    Pelo menos 1 caractere minúsculo;
    Pelo menos um caractere especial.\n
    Fornece outra tentativa ao usuário até que ele digite uma senha
    válida, informando quais requisitos faltam.
    """

    while True:
        password = ask('Digite sua senha: ').strip()

        has_size_min = len(password) >= 8
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)

        if not has_size_min:
            print('A senha deve ter pelo menos 8 caracteres. ')
        if not has_upper:
            print('A senha deve ter pelo menos um caractere maiúsculo. ')
        if not has_lower:
            print('A senha deve ter pelo menos um caractere minúsculo. ')
        if not has_number:
            print('A senha deve ter pelo menos um número. ')
        if not has_special:
            print('A senha deve ter pelo menos um caractere especial. ')
        if all([has_lower, has_number, has_size_min, has_upper, has_special]):
            return password
        print()

def auth_cpf(cpf: str) -> None:
    """Calcula se o CPF recebido é válido. Levanta uma exceção caso não for."""
    
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0]*11:
        raise InvalidCpfError
    
    def calculate_digit(cpf_slice: str, /, factor: int = 10) -> str:
        rest = sum(int(num)*(factor - i) for i, num in enumerate(cpf_slice))%11
        return '0' if rest < 2 else str((11 - rest))
    
    if not (calculate_digit(cpf[:9]) == cpf[9] and calculate_digit(cpf[:10], 11) == cpf[10]):
        raise InvalidCpfError


def cpf_find(database: Path, cpf: str) -> bool:
    """Verifica se o CPF já existe no banco de dados."""
    
    with open(database, 'r', encoding='utf8') as data:
        users = json.load(data)
        if cpf in users.keys():
            return True
        return False
