# meu_app/validators.py
import re

def validar_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)
    
    # Verifica se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos são iguais (invalida o CNPJ)
    if cnpj == cnpj[0] * 14:
        return False

    # Cálculo do primeiro dígito verificador
    def calcular_digito(digs, pesos):
        soma = sum(p * int(dig) for p, dig in zip(pesos, digs))
        resto = soma % 11
        return str(0 if resto < 2 else 11 - resto)

    # Define os pesos para os cálculos dos dígitos verificadores
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    # Verifica os dígitos verificadores
    if calcular_digito(cnpj[:12], pesos1) != cnpj[12]:
        return False
    if calcular_digito(cnpj[:13], pesos2) != cnpj[13]:
        return False

    return True

