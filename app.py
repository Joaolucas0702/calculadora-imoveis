import streamlit as st
from calculadora import CalculadoraDespesasImoveis

st.set_page_config(page_title="Calculadora de Despesas de Imóveis", layout="centered")
st.title("🏠 Calculadora de Despesas de Imóveis")

calculadora = CalculadoraDespesasImoveis()

# 🔢 Funções para lidar com moeda brasileira

def converter_para_float(valor_str):
    try:
        return float(valor_str.replace(".", "").replace(",", "."))
    except:
        return 0.0

def formatar_moeda_input(valor_str):
    valor = ''.join(c for c in valor_str if c.isdigit() or c in ",")
    if not valor:
        return "0,00"
    if "," not in valor:
        valor += ",00"
    partes = valor.split(",")
    parte_int = partes[0]
    parte_int = parte_int.lstrip("0") or "0"
    parte_int_formatada = "{:,}".format(int(parte_int)).replace(",", ".")
    return f"{parte_int_formatada},{partes[1][:2].ljust(2,'0')}"

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.header("Preencha os dados abaixo:")

col1, col2 = st.columns(2)
with col1:
    valor_imovel_str = st.text_input("Valor do Imóvel (R$)", "0,00")
    valor_imovel_str = formatar_moeda_input(valor_imovel_str)
    st.write("↳ " + valor_imovel_str)

    valor_financiado_str = st.text_input("Valor Financiado (R$)", "0,00")
    valor_financiado_str = formatar_moeda_input(valor_financiado_str)
    st.write("↳ " + valor_financiado_str)

    seguro_str = st.text_input("Seguro (verificar na simulação)", "0,00")
    seguro_str = formatar_moeda_input(seguro_str)
    st.write("↳ " + seguro_str)

valor_imovel = converter_para_float(valor_imovel_str)
valor_financiado = converter_para_float(valor_financiado_str)
seguro = converter_para_float(seguro_str)

with col2:
    tipo_financiamento = st.selectbox("Tipo de Financiamento", ["SBPE", "Minha Casa Minha Vida", "Pro Cotista"])
    cidade = st.selectbox("Cidade", ["Goiânia", "Trindade", "Senador Canedo", "Aparecida de Goiânia"])
    renda_bruta = st.number_input("Renda Bruta (R$) (se for Aparecida de Goiânia)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
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
*Sobre o valor da entrada: (2,5% sobre {moeda(entrada)}) = {moeda(itbi_entrada)}*
*Sobre o valor financiado: ({aliq}% sobre {moeda(valor_financiado)}) = {moeda(itbi_fin)}*
*Taxa de Expediente: {moeda(taxa_exp)}*
*Total estimado do ITBI: {moeda(resultado['ITBI'])}*
"""
        elif cidade == "Senador Canedo":
            itbi_detalhe = f"""
*1,5% sobre a entrada ({moeda(entrada)}) + 0,5% sobre o valor financiado ({moeda(valor_financiado)})*
*Taxa de Expediente: {moeda(8.50)}*
*Total estimado do ITBI: {moeda(resultado['ITBI'])}*
"""
        elif cidade == "Trindade":
            base = valor_imovel * 0.02
            itbi_detalhe = f"""
*2% sobre o valor do imóvel ({moeda(valor_imovel)}) = {moeda(base)}*
*Taxa de Expediente: {moeda(4.50)}*
*Total estimado do ITBI: {moeda(resultado['ITBI'])}*
"""
        elif cidade == "Goiânia":
            base = valor_imovel * 0.02
            itbi_detalhe = f"""
*2% sobre o valor do imóvel ({moeda(valor_imovel)}) = {moeda(base)}*
*Taxa de Expediente: {moeda(100)}*
*Total estimado do ITBI: {moeda(resultado['ITBI'])}*
"""
        else:
            itbi_detalhe = "*Detalhamento indisponível para esta cidade.*"

        texto = f"""
*CÁLCULO PARA COMPRA DE IMÓVEL COM FINANCIAMENTO*

*Dados do Imóvel e Financiamento*

* Valor de Compra e Venda: {moeda(valor_imovel)}
* Valor Financiado: {moeda(valor_financiado)}
* Valor de Entrada: {moeda(entrada)}
* Tipo de Financiamento: {tipo_financiamento}

*Despesas Relacionadas à Compra do Imóvel*

1️⃣ *Caixa Econômica Federal – {moeda(resultado['Lavratura'])}*  
Esse valor corresponde à lavratura do contrato de financiamento/escritura, avaliação do imóvel e relacionamento. 

2️⃣ *ITBI – Prefeitura – {moeda(resultado['ITBI'])}*  
O Imposto sobre Transmissão de Bens Imóveis (ITBI) pode ser cobrado separadamente sobre o valor do imóvel e sobre o valor financiado, dependendo da legislação municipal.

{itbi_detalhe}

3️⃣ *Cartório de Registro de Imóveis – {moeda(resultado['Registro'])}*  
Esse valor refere-se ao registro do contrato de financiamento, obrigatório para garantir a legalidade da compra e a segurança jurídica do comprador.

✅ Desconto de 50% aplicado? {'(X) Sim' if primeiro_imovel else '( ) Não'}

💡 Desconto: Se for o primeiro imóvel residencial financiado pelo SFH (Sistema Financeiro de Habitação), pode haver um desconto de 50% na taxa de registro.

💡 Obs.: O cálculo foi feito com base no valor de compra e financiamento, mas pode mudar caso a avaliação da Prefeitura seja maior ou o imóvel tenha mais de uma matrícula.

*Total Geral das Despesas*

💰 *Aproximadamente {moeda(resultado['Total Despesas'])}*

⚠️ *Aviso Importante:*  
A Suporte Soluções Imobiliárias não é responsável pelo cálculo oficial das despesas relacionadas à compra do imóvel. O presente levantamento tem caráter informativo e visa apenas auxiliar o cliente a entender os custos envolvidos na aquisição, com base em valores estimados.

Para obter informações precisas e realizar os pagamentos, recomenda-se entrar em contato com os órgãos responsáveis, como Prefeitura e o Cartório de Registro de Imóveis.
"""

        st.text_area("Resultado do Cálculo:", value=texto, height=650)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")
