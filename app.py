import streamlit as st
from calculadora import CalculadoraDespesasImoveis

st.set_page_config(page_title="Calculadora de Despesas de Imóveis", layout="centered")
st.title("🏠 Calculadora de Despesas de Imóveis")

calculadora = CalculadoraDespesasImoveis()

st.header("Preencha os dados abaixo:")

col1, col2 = st.columns(2)
with col1:
    valor_imovel = st.number_input("Valor do Imóvel (R$)", min_value=0.0, value=0.0)
    valor_financiado = st.number_input("Valor Financiado (R$)", min_value=0.0, value=0.0)
    seguro = st.number_input("Seguro (verificar na simulação)", min_value=0.0, value=0.0)

with col2:
    tipo_financiamento = st.selectbox("Tipo de Financiamento", ["SBPE", "Minha Casa Minha Vida", "Pro Cotista"])
    cidade = st.selectbox("Cidade", ["Goiânia", "Trindade", "Senador Canedo", "Aparecida de Goiânia"])
    renda_bruta = st.number_input("Renda Bruta (R$) (se for Aparecida de Goiânia)", min_value=0.0, value=0.0)
    primeiro_imovel = st.checkbox("É o primeiro imóvel financiado?", value=True)

if st.button("Calcular"):
    try:
        if cidade == "Aparecida de Goiânia":
            resultado = calculadora.calcular_aparecida(
                valor_imovel, valor_financiado, tipo_financiamento, renda_bruta, seguro, primeiro_imovel
            )
        else:
            resultado = calculadora.calcular_goiania_trindade_canedo(
                valor_imovel, valor_financiado, tipo_financiamento, cidade, seguro, primeiro_imovel
            )

        entrada = valor_imovel - valor_financiado

        # Detalhamento do ITBI com base na cidade
        if cidade == "Aparecida de Goiânia":
            itbi_entrada = entrada * 0.025
            if renda_bruta <= 4400:
                aliq = 0.5
            elif renda_bruta <= 8000:
                aliq = 1
            else:
                aliq = 1.5
            itbi_fin = valor_financiado * (aliq / 100)
            taxa_exp = 30.00
            itbi_detalhe = f"""
*Sobre o valor da entrada: (2,5% sobre R$ {entrada:,.2f}) = R$ {itbi_entrada:,.2f}*

*Sobre o valor financiado: ({aliq}% sobre R$ {valor_financiado:,.2f}) = R$ {itbi_fin:,.2f}*

*Taxa de Expediente: R$ {taxa_exp:.2f}*

*Total estimado do ITBI: R$ {resultado['ITBI']:,.2f}*
"""
        elif cidade == "Senador Canedo":
            itbi_detalhe = f"""
*1,5% sobre a entrada (R$ {entrada:,.2f}) + 0,5% sobre o valor financiado (R$ {valor_financiado:,.2f})*

*Taxa de Expediente: R$ 8,50*

*Total estimado do ITBI: R$ {resultado['ITBI']:,.2f}*
"""
        elif cidade == "Trindade":
            base = valor_imovel * 0.02
            itbi_detalhe = f"""
*2% sobre o valor do imóvel (R$ {valor_imovel:,.2f}) = R$ {base:,.2f}*

*Taxa de Expediente: R$ 4,50*

*Total estimado do ITBI: R$ {resultado['ITBI']:,.2f}*
"""
        elif cidade == "Goiânia":
            base = valor_imovel * 0.02
            itbi_detalhe = f"""
*2% sobre o valor do imóvel (R$ {valor_imovel:,.2f}) = R$ {base:,.2f}*

*Taxa de Expediente: R$ 100,00*

*Total estimado do ITBI: R$ {resultado['ITBI']:,.2f}*
"""
        else:
            itbi_detalhe = "*Detalhamento indisponível para esta cidade.*"

        texto = f"""
*CÁLCULO PARA COMPRA DE IMÓVEL COM FINANCIAMENTO*

*Dados do Imóvel e Financiamento*

* Valor de Compra e Venda: R$ {valor_imovel:,.2f}
* Valor Financiado: R$ {valor_financiado:,.2f}
* Valor de Entrada: R$ {entrada:,.2f}
* Tipo de Financiamento: {tipo_financiamento}

*Despesas Relacionadas à Compra do Imóvel*

1️⃣ *Caixa Econômica Federal – R$ {resultado['Lavratura']:,.2f}*  
Esse valor corresponde à lavratura do contrato de financiamento/escritura, avaliação do imóvel e relacionamento. 

2️⃣ *ITBI – Prefeitura – R$ {resultado['ITBI']:,.2f}*  
O Imposto sobre Transmissão de Bens Imóveis (ITBI) pode ser cobrado separadamente sobre o valor do imóvel e sobre o valor financiado, dependendo da legislação municipal.

{itbi_detalhe}

3️⃣ *Cartório de Registro de Imóveis – R$ {resultado['Registro']:,.2f}*  
Esse valor refere-se ao registro do contrato de financiamento, obrigatório para garantir a legalidade da compra e a segurança jurídica do comprador.

✅ Desconto de 50% aplicado? {'(X) Sim' if primeiro_imovel else '(X) Não'}

💡 Desconto: Se for o primeiro imóvel residencial financiado pelo SFH (Sistema Financeiro de Habitação), pode haver um desconto de 50% na taxa de registro.

💡 Obs.: O cálculo foi feito com base no valor de compra e financiamento, mas pode mudar caso a avaliação da Prefeitura seja maior ou o imóvel tenha mais de uma matrícula.

*Total Geral das Despesas*

💰 *Aproximadamente R$ {resultado['Total Despesas']:,.2f}*

⚠️ *Aviso Importante:*  
A Suporte Soluções Imobiliárias não é responsável pelo cálculo oficial das despesas relacionadas à compra do imóvel. O presente levantamento tem caráter informativo e visa apenas auxiliar o cliente a entender os custos envolvidos na aquisição, com base em valores estimados.

Para obter informações precisas e realizar os pagamentos, recomenda-se entrar em contato com os órgãos responsáveis, como Prefeitura e o Cartório de Registro de Imóveis.
"""
        st.text_area("Resultado do Cálculo:", value=texto, height=650)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")




