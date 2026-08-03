import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(
    page_title="Moda & Personalidade",
    page_icon="👔",
    layout="wide"
)

# Navegação entre Páginas / Abas
st.sidebar.title("📌 Navegação")
pagina = st.sidebar.radio("Ir para:", ["🏠 Home (Apresentação)", "📊 Dashboard Interativo"])

# ==========================================
# PARTE DO INTEGRANTE A: HOME / APRESENTAÇÃO
# ==========================================
if pagina == "🏠 Home (Apresentação)":
    st.title("👔 Identidade e Expressão: A Moda Como Espelho da Personalidade")
    st.caption("Projeto desenvolvido para a disciplina de TPAE II - UFPB")
    
    st.divider()
    
    # Seção 1: Apresentação do Projeto
    st.header("🎯 Sobre o Projeto")
    st.write("""
    A moda constitui uma importante forma de comunicação não verbal, desempenhando um papel 
    significativo na construção da identidade e na expressão da personalidade. Mais do que 
    atender à necessidade básica de vestir, o vestuário permite que os indivíduos expressem 
    valores, comportamentos e sentimento de pertencimento social.
    """)
    
    # Seção 2: Objetivos
    st.header("📌 Problema e Objetivos")
    st.markdown("""
    * **Problema de Pesquisa:** De que maneira as escolhas de vestuário, no cenário contemporâneo, expressam os traços de personalidade dos indivíduos?
    * **Objetivo Geral:** Analisar como a moda atua como forma de expressão da identidade e espelho da personalidade, investigando como as escolhas de vestuário refletem características individuais no público jovem.
    """)
    
    st.divider()
    
    # Seção 3: Descrição do Dataset
    st.header("📁 Descrição dos Dados (Dataset)")
    st.write("""
    Os dados utilizados nesta pesquisa foram obtidos via plataforma **Kaggle**, reunindo informações 
    sobre preferências de estilo, hábitos de consumo e características comportamentais.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Origem dos Dados", "Kaggle")
    col2.metric("Tratamento de Dados", "Python (Pandas)")
    col3.metric("Foco da Amostra", "Público Jovem")

# ==========================================
# PARTE DOS OUTROS INTEGRANTES: DASHBOARD
# ==========================================
elif pagina == "📊 Dashboard Interativo":
    st.title("📊 Análise Visual de Dados")
    st.write("Aqui entram os gráficos e filtros interativos (Parte do Integrante B/C).")
