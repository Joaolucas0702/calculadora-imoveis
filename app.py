import streamlit as st
from pathlib import Path
import urllib.parse
import re

# Configurações da página
st.set_page_config(page_title="Calculadora de Despesas", layout="centered")

# Caminho para o arquivo de logo
logo_path = Path("logo.png")

# Verifica se o arquivo existe e exibe a imagem
if logo_path.exists():
    st.image(str(logo_path), width=300)
else:
    st.warning("Logo não encontrada!")

from calculadora import CalculadoraDespesasImoveis

st.title("🏠 Calculadora de Despesas")

calculadora = CalculadoraDespesasImoveis()

# Funções auxiliares
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
    parte_int = partes[0].lstrip("0") or "0"
    parte_int_formatada = "{:,}".format(int(parte_int)).replace(",", ".")
    return f"{parte_int_formatada},{partes[1][:2].ljust(2,'0')}"

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

def limpar_markdown_para_copia(texto_md):
    texto_limpo = re.sub(r'\*\*(.*?)\*\*', r'\1', texto_md)
    texto_limpo = re.sub(r'\*(.*?)\*', r'\1', texto_limpo)
    texto_limpo = texto_limpo.replace("R$ R$", "R$ ")
    texto_limpo = re.sub(r'\n\s*\n', '\n\n', texto_limpo)
    return texto_limpo

def botao_whatsapp(mensagem):
    mensagem_encoded = urllib.parse.quote(mensagem)
    link = f"https://wa.me/?text={mensagem_encoded}"
    html_link = f'<a href="{link}" target="_blank" style="text-decoration:none;display:inline-block;margin-top:10px;background:#25D366;color:white;padding:10px 20px;border-radius:8px;font-weight:bold;">📲 Compartilhar no WhatsApp</a>'
    st.markdown(html_link, unsafe_allow_html=True)

# Formulário
st.header("Preencha os dados abaixo:")

col1, col2 = st.columns(2)
with col1:
    valor_imovel_str = st.text_input("Valor do Imóvel (R$)", "0,00")
    valor_imovel_str = formatar_moeda_input(valor_imovel_str)
    st.write("↓ " + valor_imovel_str)

    valor_financiado_str = st.text_input("Valor Financiado (R$)", "0,00")
    valor_financiado_str = formatar_moeda_input(valor_financiado_str)
    st.write("↓ " + valor_financiado_str)

    seguro_str = st.text_input("Seguro (verificar na simulação)", "0,00")
    seguro_str = formatar_moeda_input(seguro_str)
    st.write("↓ " + seguro_str)

valor_imovel = converter_para_float(valor_imovel_str)
valor_financiado = converter_para_float(valor_financiado_str)
seguro = converter_para_float(seguro_str)

with col2:
    tipo_financiamento = st.selectbox("Tipo de Financiamento", ["SBPE", "Minha Casa Minha Vida", "Pro Cotista"])
    cidade = st.selectbox("Cidade", ["Goiânia - GO", "Trindade - GO", "Senador Canedo - GO", "Aparecida de Goiânia - GO"])

    if cidade == "Aparecida de Goiânia - GO":
        renda_bruta = st.number_input("Renda Bruta (R$)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
    else:
        renda_bruta = 0.0
        st.info("O campo de Renda Bruta só é necessário para Aparecida de Goiânia - GO.")

    primeiro_imovel = st.checkbox("É o primeiro imóvel financiado?", value=True)

if st.button("Calcular"):
    try:
        if cidade == "Aparecida de Goiânia - GO":
            resultado = calculadora.calcular_aparecida(
                valor_imovel, valor_financiado, tipo_financiamento, renda_bruta, seguro, primeiro_imovel, cidade
            )
        else:
            resultado = calculadora.calcular_goiania_trindade_canedo(
                valor_imovel, valor_financiado, tipo_financiamento, cidade, seguro, primeiro_imovel
            )

        entrada = valor_imovel - valor_financiado

        # (aqui continua sua lógica para itbi_detalhe e texto)

        texto = f"""
 📟 **CÁLCULO PARA COMPRA DE IMÓVEL COM FINANCIAMENTO**

 🏡 **Dados do Imóvel e Financiamento**

- **Valor de Compra e Venda:**  {moeda(valor_imovel)}
- **Valor Financiado:**  {moeda(valor_financiado)}
- **Valor de Entrada:**  {moeda(entrada)}
- **Tipo de Financiamento:** {tipo_financiamento}

 💰 **Despesas Relacionadas à Compra do Imóvel**

1️⃣ **Caixa Econômica Federal – {moeda(resultado['Lavratura'])}**

Esse valor corresponde à lavratura do contrato de financiamento/escritura, avaliação do imóvel e relacionamento. 

2️⃣ **ITBI – Prefeitura – {moeda(resultado['ITBI'])}** 

O ITBI pode ser cobrado separadamente sobre o valor do imóvel e sobre o valor financiado, dependendo da legislação municipal.

Obs.: Caso a avaliação do imóvel feita pela Prefeitura fique maior do que o valor de compra e venda esse valor sofrerá alteração.

{itbi_detalhe}

3️⃣ **Cartório de Registro de Imóveis – {moeda(resultado['Registro'])}** 

Esse valor refere-se ao registro da compra/venda do imóvel e alienação fiduciária.

Obs.: Este cálculo foi feito pelo valor de compra e venda e valor de financiamento. Caso a avaliação feita pela Prefeitura fique maior ou o imóvel tenha mais de uma matrícula, esse cálculo sofrerá alteração.

✅ **Desconto de 50% aplicado?** {'Sim ✅' if primeiro_imovel else 'Não ❌'}

💡 **Obs.:** *Se for o primeiro imóvel residencial financiado pelo SFH, pode haver um desconto de 50% nas custas de registro.*

 💵 **Total Geral das Despesas**

**Total geral estimado:** {moeda(resultado['Total Despesas'])}

⚠️ **Aviso Importante:**

*A Suporte Soluções Imobiliárias não é responsável pelo cálculo oficial das despesas relacionadas à compra do imóvel. O presente levantamento tem caráter informativo e visa apenas auxiliar o cliente a entender os custos envolvidos na aquisição, com base em valores estimados.*

*Para obter informações precisas e realizar os pagamentos, recomenda-se entrar em contato com os órgãos responsáveis, como Prefeitura e o Cartório de Registro de Imóveis.*
"""

        st.markdown(texto)
        texto_para_copiar = limpar_markdown_para_copia(texto)

        st.components.v1.html(f"""
        <style>
        .copiar-btn {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-top: 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        .copiar-btn:hover {{
            background-color: #45a049;
        }}
        </style>

        <textarea id="textoResultado" style="display:none;">{texto_para_copiar}</textarea>
        <button class="copiar-btn" onclick="navigator.clipboard.writeText(document.getElementById('textoResultado').value)">📋 Copiar para a área de transferência</button>
        """, height=80)

        # Botão para compartilhar no WhatsApp
        botao_whatsapp(texto_para_copiar)

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")

