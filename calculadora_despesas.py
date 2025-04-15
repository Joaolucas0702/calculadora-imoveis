def calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel=False):
    tabela_registro = [
        (625.89, 111),
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
        faixa_valida = 0
        for limite, custo_reg in tabela_registro:
            if valor >= limite:
                faixa_valida = custo_reg
            else:
                break
        return faixa_valida

    custo_imovel = custo(valor_imovel)
    custo_financiado = custo(valor_financiado)
    total = custo_imovel + custo_financiado

    # Soma os R$ 200 fixos fora do desconto
    total += 200

    # Aplica o desconto de 50% apenas na parte do custo original, não no extra
    if primeiro_imovel:
        total = (custo_imovel + custo_financiado) * 0.5 + 200

    return round(total, 2)

