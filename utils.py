from os import system, name

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
