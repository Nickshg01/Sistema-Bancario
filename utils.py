from os import system, name
import json
from pathlib import Path

def ask(msg: str) -> str:
    """Cria um input para que o usuário dê uma entrada. 
    Após coletar a entrada do usuário, a função limpa o terminal\n
    Verifica se o campo não está em branco"""

    while True:
        var = input(msg).strip()
        system('cls' if name == 'nt' else 'clear')

        if not var:
            print('Você deixou este campo vazio.\n')
            continue
        return var
    
    
def money_format(money: float) -> float:
    """Retorna o dinheiro formatado para a moeda Real."""
    return f'R$ {money:,.2f}'.replace(',', 'j').replace('.', ',').replace('j', '.')


def validate_num(msg: str, type: type = float) -> float:
    """Verifica se a entrada do usuário pode ser convertida para float. Caso contrário, pede outra entrada ao usuário."""
    while True:
        try:
            var = type(ask(msg))
            return var
        
        except ValueError:
            print('Digite apenas números.\n')


def update_data(database: Path, cpf: str, **kwargs) -> None:
    """Atualiza o banco de dados de um usuário."""

    with open(database, 'r', encoding='utf8') as file:
        data = json.load(file)
    data[cpf].update(kwargs)

    with open(database, 'w', encoding='utf8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
