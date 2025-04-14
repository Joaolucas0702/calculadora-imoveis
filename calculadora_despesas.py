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
        for limite, custo in tabela_registro:
            if valor <= limite:
                return custo
        return tabela_registro[-1][1]

    custo_imovel = custo(valor_imovel)
    custo_financiado = custo(valor_financiado)

    total = custo_imovel + custo_financiado

    if primeiro_imovel:
        total *= 0.5

    return round(total, 2)


class CalculadoraDespesasImoveis:
    def calcular_goiania_trindade_canedo(self, valor_imovel, valor_financiado, tipo_financiamento, cidade, seguro, primeiro_imovel):
        entrada = valor_imovel - valor_financiado

        itbi = calcular_itbi(cidade, valor_imovel, valor_financiado)
        lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_financiado)
        registro = calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel)

        total_despesas = itbi + lavratura + registro + seguro

        return {
            "Entrada": entrada,
            "ITBI": itbi,
            "Lavratura": lavratura,
            "Registro": registro,
            "Seguro (conferir na simulação)": seguro,
            "Total Despesas": total_despesas
        }

    def calcular_aparecida(self, valor_imovel, valor_financiado, tipo_financiamento, renda_bruta, seguro, primeiro_imovel):
        entrada = valor_imovel - valor_financiado

        itbi = calcular_itbi("Aparecida de Goiânia", valor_imovel, valor_financiado, renda_bruta)
        lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_financiado)
        registro = calcular_registro_cartorio(valor_imovel, valor_financiado, primeiro_imovel)

        total_despesas = itbi + lavratura + registro + seguro

        return {
            "Entrada": entrada,
            "ITBI": itbi,
            "Lavratura": lavratura,
            "Registro": registro,
            "Seguro (conferir na simulação)": seguro,
            "Total Despesas": total_despesas
        }
