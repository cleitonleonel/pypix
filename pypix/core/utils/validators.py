import re


def validate_cpf(numbers):
    """ Valida CPF brasileiro (Cadastro de Pessoas Físicas).
    Args:
        numbers (str): Número do CPF como string, pode incluir caracteres não numéricos.
    Returns:
        bool: True se o CPF for válido, false caso contrário.
    """

    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def validate_phone(value):
    """ Valida número de telefone brasileiro.
    Args:
        value (str): Número de telefone como string, pode incluir caracteres não numéricos.
    Returns:
        bool: True se o telefone for válido, false caso contrário.
    """

    rule = re.compile(r'^\+?[1-9]\d{1,14}$')
    return bool(rule.match(value))
