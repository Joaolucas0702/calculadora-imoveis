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
    # Cada tupla representa: (limite superior da faixa, custo correspondente)
    tabela_registro = [
        (625.89, 73.22),
        (1251.79, 111.00),
        (2503.58, 141.69),
        (5007.15, 205.48),
        (10014.30, 403.86),
        (15021.47, 432.19),
        (25035.77, 550.29),
        (37553.65, 696.73),
        (50071.55, 923.45),
        (62589.43, 1098.21),
        (100143.09, 1539.87),
        (150214.64, 2314.53),
        (250357.73, 3117.53),
        (375536.58, 4092.94),
        (500715.44, 4822.74),
        (751073.17, 5788.70),
        (1126609.75, 6936.52),
        (1502146.34, 8065.44),
        (float('inf'), 8810.65),
    ]

    def custo(valor):
        for limite, custo_faixa in tabela_registro:
            if valor <= limite:
                return custo_faixa
        return tabela_registro[-1][1]  # fallback (não deveria chegar aqui)

    custo_imovel = custo(valor_imovel)
    custo_financiado = custo(valor_financiado)
    total = custo_imovel + custo_financiado

    # R$ 200 fixos fora do desconto
    total += 200

    # Aplica 50% de desconto sobre os custos principais se for o primeiro imóvel
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

