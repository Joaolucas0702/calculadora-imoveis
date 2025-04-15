def calcular_itbi(cidade, valor_imovel, valor_financiado, renda_bruta=None, taxa_expediente_padrao=100):
    entrada = valor_imovel - valor_financiado

    if cidade == "Aparecida de Goiânia - GO":
        taxa_expediente = 30
        itbi_entrada = entrada * 0.025

        if renda_bruta is None:
            raise ValueError("Renda bruta é obrigatória para Aparecida de Goiânia - GO.")

        if renda_bruta <= 4400:
            itbi_financiado = valor_financiado * 0.005
        elif renda_bruta <= 8000:
            itbi_financiado = valor_financiado * 0.01
        else:
            itbi_financiado = valor_financiado * 0.015

        itbi = itbi_entrada + itbi_financiado

    elif cidade == "Senador Canedo - GO":
        if valor_financiado <= 500000:
            aliquota_financiado = 0.005
        elif valor_financiado <= 1000000:
            aliquota_financiado = 0.01
        elif valor_financiado <= 1500000:
            aliquota_financiado = 0.015
        else:
            aliquota_financiado = 0.02

        itbi_financiado = valor_financiado * aliquota_financiado
        itbi_entrada = entrada * 0.02
        itbi = itbi_entrada + itbi_financiado
        taxa_expediente = 8.50

    elif cidade == "Trindade - GO":
        itbi = valor_imovel * 0.02
        taxa_expediente = 4.50

    elif cidade == "Goiânia - GO":
        itbi = valor_imovel * 0.02
        taxa_expediente = taxa_expediente_padrao

    else:
        itbi = 0
        taxa_expediente = 0

    return itbi + taxa_expediente


def calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel=False):
    tabela_registro = [
        (0.00, 73.22),
        (625.89, 111.00),
        (1251.79, 141.69),
        (2503.58, 205.48),
        (5007.15, 403.86),
        (10014.30, 432.19),
        (15021.47, 550.29),
        (25035.77, 696.73),
        (37553.65, 923.45),
        (50071.55, 1098.21),
        (62589.43, 1539.87),
        (100143.09, 2314.53),
        (150214.64, 3117.53),
        (250357.73, 4092.94),
        (375536.58, 4822.74),
        (500715.44, 5788.70),
        (751073.17, 6936.52),
        (1126609.75, 8065.44),
        (1502146.34, 8610.85),
    ]

    def custo(valor):
        for limite, custo_reg in tabela_registro:
            if valor <= limite:
                return custo_reg
        # Se o valor for maior que todos os limites, aplica o último custo
        return tabela_registro[-1][1]

    custo_imovel = custo(valor_imovel)
    custo_financiado = custo(valor_financiado)
    total = custo_imovel + custo_financiado

    # Soma os R$ 200 fixos fora do desconto
    total += 200

    # Aplica o desconto de 50% apenas na parte original, não no extra
    if primeiro_imovel:
        total = (custo_imovel + custo_financiado) * 0.5 + 200

    return round(total, 2)



def calcular_lavratura_contrato(tipo_financiamento, valor_financiado):
    if tipo_financiamento in ["Minha Casa Minha Vida", "Pro Cotista"]:
        return valor_financiado * 0.01 + valor_financiado * 0.015
    elif tipo_financiamento == "SBPE":
        return valor_financiado * 0.01 + 842
    else:
        return 0


    return round(total, 2)

