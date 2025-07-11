import streamlit as st
from calculadora_despesas import (
    calcular_itbi,
    calcular_registro_cartorio,
    calcular_lavratura_contrato,
    calcular_escritura
)

def formatar_br(valor):
    """Formata valores como R$ 1.234,56"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    st.set_page_config(page_title="Calculadora de Despesas", layout="centered")
    st.title("🏠 Calculadora de Despesas Imobiliárias")

    # Seleção do tipo de operação
    tipo_operacao = st.selectbox(
        "Tipo de Operação",
        ["Compra com financiamento", "Compra à vista", "Empréstimo com imóvel de garantia"]
    )

    # Campo comum - Valor do Imóvel
    valor_imovel = st.number_input(
        "Valor total do imóvel (R$)", 
        min_value=0.0,
        value=250000.0,
        step=1000.0,
        format="%.2f"
    )

    # Campos específicos por operação
    if tipo_operacao == "Compra com financiamento":
        primeiro_imovel = st.checkbox("Primeiro imóvel? (50% de desconto no registro)")
        seguro = st.number_input(
            "Seguro (R$)",
            min_value=0.0,
            value=1500.0,
            step=50.0,
            format="%.2f"
        )
        valor_financiado = st.number_input(
            "Valor financiado (R$)", 
            min_value=0.0,
            max_value=valor_imovel,
            value=min(valor_imovel * 0.8, valor_imovel),
            step=1000.0,
            format="%.2f"
        )
        tipo_financiamento = st.selectbox(
            "Tipo de financiamento", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )
        cidade = st.selectbox(
            "Cidade", 
            ["Goiânia", "Trindade", "Aparecida de Goiânia", "Senador Canedo"]
        )
        
        if cidade == "Aparecida de Goiânia":
            renda_bruta = st.number_input(
                "Renda bruta mensal (R$)", 
                min_value=0.0,
                value=5000.0,
                step=100.0,
                format="%.2f"
            )

        if st.button("🟢 Calcular Despesas", type="primary"):
            itbi = calcular_itbi(cidade, valor_imovel, valor_financiado, renda_bruta if cidade == "Aparecida de Goiânia" else None)
            lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_financiado)
            registro = calcular_registro_cartorio(valor_imovel, primeiro_imovel)
            total = itbi + lavratura + registro + seguro
            
            st.subheader("📋 Resultado para Compra com Financiamento")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valor do Imóvel", formatar_br(valor_imovel))
                st.metric("Entrada", formatar_br(valor_imovel - valor_financiado))
            with col2:
                st.metric("Valor Financiado", formatar_br(valor_financiado))
                st.metric("Tipo de Financiamento", tipo_financiamento)
            
            st.divider()
            st.subheader("📝 Detalhes das Despesas")
            
            # ITBI
            st.markdown(f"""
            **📌 ITBI (Imposto sobre Transmissão de Bens Imóveis)**
            - *O que é*: Imposto municipal sobre a transação
            - *Cálculo*: {2.5 if cidade in ['Aparecida de Goiânia', 'Senador Canedo'] else 2}% sobre R$ {valor_imovel - valor_financiado:,.2f}
            - *Valor*: {formatar_br(itbi)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            # Lavratura
            st.markdown(f"""
            **📌 Lavratura de Contrato**
            - *O que é*: Custos cartoriais para elaboração do contrato
            - *Cálculo*: {{
                'SBPE': '0.3% do financiado (mín. R$ 1.000)',
                'MCMV': '0.25% do financiado (mín. R$ 800)',
                'Pro Cotista': '0.35% do financiado (mín. R$ 1.200)'
            }}[tipo_financiamento]
            - *Valor*: {formatar_br(lavratura)}
            """)
            
            # Registro
            st.markdown(f"""
            **📌 Registro no Cartório**
            - *O que é*: Taxa para registrar a transação no RGI
            - *Base*: Maior valor entre imóvel e financiado (R$ {max(valor_imovel, valor_financiado):,.2f})
            - *Desconto*: {'Sim (50%)' if primeiro_imovel else 'Não'}
            - *Valor*: {formatar_br(registro)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            # Seguro
            st.markdown(f"""
            **📌 Seguro**
            - *O que é*: Seguro obrigatório do financiamento
            - *Valor*: {formatar_br(seguro)}
            """)
            
            st.divider()
            st.success(f"**💵 TOTAL DE DESPESAS:** {formatar_br(total)}")

    elif tipo_operacao == "Compra à vista":
        cidade = st.selectbox(
            "Cidade", 
            ["Goiânia", "Trindade", "Aparecida de Goiânia", "Senador Canedo"]
        )
        
        if st.button("🟢 Calcular Despesas", type="primary"):
            escritura = calcular_escritura(valor_imovel)
            registro = calcular_registro_cartorio(valor_imovel, False)
            itbi = calcular_itbi(cidade, valor_imovel)
            total = itbi + escritura + registro
            
            st.subheader("📋 Resultado para Compra à Vista")
            st.metric("Valor do Imóvel", formatar_br(valor_imovel))
            
            st.divider()
            st.subheader("📝 Detalhes das Despesas")
            
            # Escritura
            st.markdown(f"""
            **📌 Escritura Pública**
            - *O que é*: Documento que formaliza a compra no tabelionato
            - *Base*: Valor do imóvel (R$ {valor_imovel:,.2f})
            - *Valor*: {formatar_br(escritura)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            # ITBI
            st.markdown(f"""
            **📌 ITBI (Imposto sobre Transmissão de Bens Imóveis)**
            - *O que é*: Imposto municipal sobre a transação
            - *Alíquota*: {{
                'Goiânia': '2%',
                'Trindade': '2%',
                'Aparecida de Goiânia': '2.5%',
                'Senador Canedo': '2.5%'
            }}[cidade]
            - *Cálculo*: {2.5 if cidade in ['Aparecida de Goiânia', 'Senador Canedo'] else 2}% sobre R$ {valor_imovel:,.2f}
            - *Valor*: {formatar_br(itbi)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            # Registro
            st.markdown(f"""
            **📌 Registro no Cartório**
            - *O que é*: Taxa para registrar a propriedade no RGI
            - *Base*: Valor do imóvel (R$ {valor_imovel:,.2f})
            - *Valor*: {formatar_br(registro)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            st.divider()
            st.success(f"**💵 TOTAL DE DESPESAS:** {formatar_br(total)}")

    elif tipo_operacao == "Empréstimo com imóvel de garantia":
        primeiro_imovel = st.checkbox("Primeiro imóvel? (50% de desconto no registro)")
        seguro = st.number_input(
            "Seguro (R$)",
            min_value=0.0,
            value=1500.0,
            step=50.0,
            format="%.2f"
        )
        valor_emprestimo = st.number_input(
            "Valor do empréstimo (R$)", 
            min_value=0.0,
            max_value=valor_imovel,
            value=valor_imovel * 0.6,
            step=1000.0,
            format="%.2f"
        )
        tipo_financiamento = st.selectbox(
            "Tipo de operação", 
            ["SBPE", "MCMV", "Pro Cotista"]
        )

        if st.button("🟢 Calcular Despesas", type="primary"):
            lavratura = calcular_lavratura_contrato(tipo_financiamento, valor_emprestimo)
            registro = calcular_registro_cartorio(valor_imovel, primeiro_imovel)
            total = lavratura + registro + seguro
            
            st.subheader("📋 Resultado para Empréstimo com Garantia")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valor do Imóvel", formatar_br(valor_imovel))
            with col2:
                st.metric("Valor do Empréstimo", formatar_br(valor_emprestimo))
            
            st.divider()
            st.subheader("📝 Detalhes das Despesas")
            
            # Lavratura
            st.markdown(f"""
            **📌 Lavratura de Contrato**
            - *O que é*: Custos cartoriais para elaboração do contrato
            - *Cálculo*: {{
                'SBPE': '0.3% do empréstimo (mín. R$ 1.000)',
                'MCMV': '0.25% do empréstimo (mín. R$ 800)',
                'Pro Cotista': '0.35% do empréstimo (mín. R$ 1.200)'
            }}[tipo_financiamento]
            - *Valor*: {formatar_br(lavratura)}
            """)
            
            # Registro
            st.markdown(f"""
            **📌 Registro da Garantia**
            - *O que é*: Taxa para registrar o financiamento no RGI
            - *Base*: Valor do imóvel (R$ {valor_imovel:,.2f})
            - *Desconto*: {'Sim (50%)' if primeiro_imovel else 'Não'}
            - *Valor*: {formatar_br(registro)}
            """.replace(",", "X").replace(".", ",").replace("X", "."))
            
            # Seguro
            st.markdown(f"""
            **📌 Seguro**
            - *O que é*: Seguro obrigatório da operação
            - *Valor*: {formatar_br(seguro)}
            """)
            
            st.divider()
            st.success(f"**💵 TOTAL DE DESPESAS:** {formatar_br(total)}")

if __name__ == "__main__":
    main()

    except Exception as e:
        st.error(f"Erro ao calcular: {e}")
