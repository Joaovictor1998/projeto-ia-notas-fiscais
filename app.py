import streamlit as st
import pandas as pd
import zipfile
import xml.etree.ElementTree as ET
import joblib

st.set_page_config(page_title="Dashboard de Notas Fiscais", layout="wide")

st.title("📊 Gestão Financeira Jra Sistema de Incêndio.")
st.markdown("JRA SISTEMA DE INCÊNDIO.")

def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    if "password_correct" not in st.session_state:
        # Inicializa a tela de login
        st.text_input("Senha do Sistema", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Senha do Sistema", type="password", on_change=password_entered, key="password")
        st.error("😕 Senha incorreta")
        return False
    else:
        return True

def password_entered():
    """Verifica se a senha digitada está correta."""
    if st.session_state["password"] == "password": # <-- TROQUE SUA SENHA AQUI
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # remove a senha do estado por segurança
    else:
        st.session_state["password_correct"] = False

# Só carrega o resto do app se a senha estiver correta
if not check_password():
    st.stop()

    
# Função de extração ajustada para o seu XML
def processar_zip(file):
    dados = []
    with zipfile.ZipFile(file, 'r') as z:
        arquivos_xml = [f for f in z.namelist() if f.endswith('.xml')]
        for arquivo in arquivos_xml:
            with z.open(arquivo) as f:
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    def find_val(tag):
                        el = root.find(f".//{{*}}{tag}")
                        return float(el.text) if el is not None else 0.0

                    def find_text(tag):
                        el = root.find(f".//{{*}}{tag}")
                        return el.text if el is not None else None

                    data_raw = find_text('DataEmissao')
                    v_bruto = find_val('ValorServicos')
                    
                    if v_bruto > 0 and data_raw:
                        dados.append({
                            'Data': pd.to_datetime(data_raw[:10]),
                            'Bruto': v_bruto,
                            'Impostos': find_val('ValorIss') + find_val('ValorInss'),
                            'Liquido': find_val('ValorLiquidoNfse')
                        })
                except Exception:
                    continue
    return pd.DataFrame(dados)

# Sidebar para upload
uploaded_file = st.sidebar.file_uploader("Escolha o arquivo ZIP", type="zip")

if uploaded_file:
    df = processar_zip(uploaded_file)
    
    if not df.empty:
        # --- SEÇÃO 1: MÉTRICAS PRINCIPAIS (KPIs) ---
        st.subheader("💰 Resumo Financeiro Geral 2025")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total de Notas", len(df))
        col2.metric("Faturamento Bruto", f"R$ {df['Bruto'].sum():,.2f}")
        col3.metric("Total Impostos", f"R$ {df['Impostos'].sum():,.2f}", delta_color="inverse")
        col4.metric("Valor Líquido", f"R$ {df['Liquido'].sum():,.2f}")
        
        st.markdown("---")

        # --- SEÇÃO 2: GRÁFICOS E PREVISÃO ---
        col_grafico, col_previsao = st.columns([2, 1])

        with col_grafico:
            st.subheader("📈 Evolução Mensal")
            df['Mes'] = df['Data'].dt.to_period('M').astype(str)
            chart_data = df.groupby('Mes')[['Bruto', 'Liquido']].sum()
            st.bar_chart(chart_data)

        with col_previsao:
            st.subheader("🔮 Previsão para 2026")
            try:
                # 1. Carrega o modelo
                modelo = joblib.load('modelos/modelo_previsao_financeira.joblib')
                
                # 2. Simulação dos 12 meses de 2026
                projeções_2025 = []
                valor_atual = chart_data['Liquido'].iloc[-1] # Começa com o último valor real de 2025
                
                for mes in range(12):
                    # O modelo prevê o próximo mês baseado no atual
                    previsao_mes = modelo.predict([[valor_atual]])[0]
                    projeções_2025.append(previsao_mes)
                    valor_atual = previsao_mes # O valor previsto vira a base para o próximo mês
                
                valor_liquido_anual_2025 = sum(projeções_2025)
                media_mensal_2025 = valor_liquido_anual_2025 / 12

                # 3. Exibição dos resultados
                st.success(f"Estimativa Total Líquida para 2026:")
                st.title(f"R$ {valor_liquido_anual_2025:,.2f}")
                
                st.metric("Média Mensal Estimada", f"R$ {media_mensal_2025:,.2f}")
                st.caption("Esta projeção utiliza o modelo de Regressão Linear para simular os 12 meses do próximo ano.")
                
            except Exception as e:
                st.warning("Para calcular 2026, certifique-se de que o modelo foi treinado.")
