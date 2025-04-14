import streamlit as st
from calculadora import CalculadoraDespesasImoveis
import urllib.parse

st.set_page_config(page_title="Calculadora de Despesas de Imóveis", layout="centered")
st.title("🏠 Calculadora de Despesas de Imóveis")

calculadora = CalculadoraDespesasImoveis()

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

def botao_whatsapp(mensagem):
    mensagem_encoded = urllib.parse.quote(mensagem)
    link = f"https://wa.me/?text={mensagem_encoded}"
    html_link = f'<a href="{link}" target="_blank">📲 Compartilhar no WhatsApp</a>'
    st.markdown(html_link, unsafe_allow_html=True)

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
            itbi_detalhe_markdown = f"""
**Sobre o valor do imóvel:** (2,5% sobre {moeda(entrada)}) = {moeda(itbi_entrada)}  
**Sobre o valor financiado:** ({aliq}% sobre {moeda(valor_financiado)}) = {moeda(itbi_fin)}  
**Taxa de Expediente da avaliação do ITBI (se aplicável):** {moeda(taxa_exp)}  
**Total estimado do ITBI:** {moeda(resultado.get('ITBI', 0.0))}
"""
            itbi_detalhe_whatsapp = f"""
Sobre o valor do imóvel: (2,5% sobre {moeda(entrada)}) = {moeda(itbi_entrada)}
Sobre o valor financiado: ({aliq}% sobre {moeda(valor_financiado)}) = {moeda(itbi_fin)}
Taxa de Expediente da avaliação do ITBI (se aplicável): {moeda(taxa_exp)}
Total estimado do ITBI: {moeda(resultado.get('ITBI', 0.0))}
"""

        elif cidade == "Senador Canedo":
            itbi_detalhe_markdown = f"""
**Sobre o valor do imóvel:** (1,5% sobre {moeda(entrada)})  
**Sobre o valor financiado:** (0,5% sobre {moeda(valor_financiado)})  
**Taxa de Expediente da avaliação do ITBI (se aplicável):** {moeda(8.50)}  
**Total estimado do ITBI:** {moeda(resultado.get('ITBI', 0.0))}
"""
            itbi_detalhe_whatsapp = f"""
Sobre o valor do imóvel: (1,5% sobre {moeda(entrada)})
Sobre o valor financiado: (0,5% sobre {moeda(valor_financiado)})
Taxa de Expediente da avaliação do ITBI (se aplicável): {moeda(8.50)}
Total estimado do ITBI: {moeda(resultado.get('ITBI', 0.0))}
"""

        elif cidade == "Trindade":
            base = valor_imovel * 0.02
            itbi_detalhe_markdown = f"""
**Sobre o valor do imóvel:** (2% sobre {moeda(valor_imovel)}) = {moeda(base)}  
**Taxa de Expediente da avaliação do ITBI (se aplicável):** {moeda(4.50)}  
**Total estimado do ITBI:** {moeda(resultado.get('ITBI', 0.0))}
"""
            itbi_detalhe_whatsapp = f"""
Sobre o valor do imóvel: (2% sobre {moeda(valor_imovel)}) = {moeda(base)}
Taxa de Expediente da avaliação do ITBI (se aplicável): {moeda(4.50)}
Total estimado do ITBI: {moeda(resultado.get('ITBI', 0.0))}
"""

        elif cidade == "Goiânia":
            base = valor_imovel * 0.02
            itbi_detalhe_markdown = f"""
**Sobre o valor do imóvel:** (2% sobre {moeda(valor_imovel)}) = {moeda(base)}  
**Taxa de Expediente da avaliação do ITBI (se aplicável):** {moeda(100)}  
**Total estimado do ITBI:** {moeda(resultado.get('ITBI', 0.0))}
"""
            itbi_detalhe_whatsapp = f"""
Sobre o valor do imóvel: (2% sobre {moeda(valor_imovel)}) = {moeda(base)}
Taxa de Expediente da avaliação do ITBI (se aplicável): {moeda(100)}
Total estimado do ITBI: {moeda(resultado.get('ITBI', 0.0))}
"""
        else:
            itbi_detalhe_markdown = "**Detalhamento indisponível para esta cidade.**"
            itbi_detalhe_whatsapp = "Detalhamento indisponível para esta cidade."

        texto = f"""
### 🧾 CÁLCULO PARA COMPRA DE IMÓVEL COM FINANCIAMENTO

#### 🏡 Dados do Imóvel e Financiamento

- **Valor de Compra e Venda:** {moeda(valor_imovel)}
- **Valor Financiado:** {moeda(valor_financiado)}
- **Valor de Entrada:** {moeda(entrada)}
- **Tipo de Financiamento:** {tipo_financiamento}

#### 💰 Despesas Relacionadas à Compra do Imóvel

**1️⃣ Caixa Econômica Federal – {moeda(resultado.get('Lavratura', 0.0))}**  
Esse valor corresponde à lavratura do contrato de financiamento/escritura, avaliação do imóvel e relacionamento.

**2️⃣ ITBI – Prefeitura – {moeda(resultado.get('ITBI', 0.0))}**  
O ITBI pode ser cobrado separadamente sobre o valor do imóvel e sobre o valor financiado, dependendo da legislação municipal.

{itbi_detalhe_markdown}

**3️⃣ Cartório de Registro de Imóveis – {moeda(resultado.get('Registro', 0.0))}**  
Esse valor refere-se ao registro do contrato de financiamento.

✅ **Desconto de 50% aplicado?** {'Sim ✅' if primeiro_imovel else 'Não ❌'}

💡 *Obs.: Se for o primeiro imóvel residencial financiado pelo SFH, pode haver um desconto de 50% na taxa de registro.*

#### 💵 Total Geral das Despesas

**Total estimado:** {moeda(resultado.get('Total Despesas', 0.0))}

⚠️ *Este cálculo é apenas uma estimativa informativa. Para valores oficiais, consulte os órgãos competentes.*
"""

        st.markdown(texto)

        texto_whatsapp = texto.replace("**", "").replace("*", "") + "\n" + itbi_detalhe_whatsapp
        botao_whatsapp(texto_whatsapp)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")
