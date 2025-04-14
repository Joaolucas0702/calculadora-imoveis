from calculadora_despesas import (
    calcular_itbi,
    calcular_registro_cartorio,
    calcular_lavratura_contrato,
)

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

