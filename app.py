import streamlit as st
from calculadora import CalculadoraDespesasImoveis
import urllib.parse
from pathlib import Path

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

        markdown_data = {
            "valor_imovel": moeda(valor_imovel),
            "valor_financiado": moeda(valor_financiado),
            "entrada": moeda(entrada),
            "tipo": tipo_financiamento,
            "lavratura": moeda(resultado.get("Lavratura", 0.0)),
            "itbi_total": moeda(resultado.get("ITBI", 0.0)),
            "aliq_imovel": "2",
            "base_imovel": moeda(valor_imovel),
            "valor_itbi_imovel": moeda(valor_imovel * 0.02),
            "aliq_financiado": "0",
            "base_financiado": moeda(0),
            "valor_itbi_financiado": moeda(0),
            "taxa_expediente": moeda(100),
            "registro": moeda(resultado.get("Registro", 0.0)),
            "desconto": "(X) Sim" if primeiro_imovel else "( ) Não",
            "total": moeda(resultado.get("Total Despesas", 0.0)),
        }

        template_markdown = Path("/mnt/data/texto_markdown.txt").read_text()
        template_whatsapp = Path("/mnt/data/texto_whatsapp.txt").read_text()

        texto_markdown = template_markdown.format(**markdown_data)
        texto_whatsapp = template_whatsapp.format(**markdown_data)

        st.markdown(texto_markdown)
        botao_whatsapp(texto_whatsapp)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")
        
