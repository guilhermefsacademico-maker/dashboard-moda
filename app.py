import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. CONFIGURAÇÃO GLOBAL DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Moda & Personalidade - UFPB",
    page_icon="👔",
    layout="wide"
)

# Estilo global dos gráficos
sns.set_theme(style="whitegrid")

# ==============================================================================
# 2. PIPELINE DE TRATAMENTO E ENGENHARIA DE DADOS (ETL)
# ==============================================================================
@st.cache_data
def carregar_e_tratar_dados(caminho_ou_arquivo):
    df_raw = pd.read_csv(caminho_ou_arquivo)
    df = df_raw.copy()

    # 1. Limpeza estrutural de espaços invisíveis nos rótulos
    df.columns = df.columns.str.strip()

    # Renomeação das variáveis para termos padronizados
    mapeamento_colunas = {
        '1.Age Group': 'Idade', 
        '2.Gender': 'Genero', 
        '3.Profession': 'Profissao',
        'Section 2: Style Preferences\n4. How would you describe your go-to daily outfit? (Select one)': 'Estilo_Diario',
        '5. What’s your favorite color palette for clothing?': 'Paleta_Cores',
        '6. Do you prioritize functionality or aesthetics in your outfits?': 'Prioridade_Uso',
        '7.Which of these best describes your wardrobe?': 'Tipo_Guarda_Roupa',
        'Section 3: Shopping Habits\n8. How often do you shop for new clothes?': 'Frequencia_Compras',
        '9.What influences your clothing purchases the most?': 'Influencia_Compra',
        '10. Where do you typically shop for clothes? (Select all that apply)': 'Local_Compras',
        'Section 4: Lifestyle\n11. How often do you attend formal events?': 'Eventos_Formais',
        '12.Do you often experiment with new styles or stick to what you know?': 'Experimenta_Estilos',
        '13. What kind of footwear do you wear most often?': 'Tipo_Calcado',
        '14. How active is your daily lifestyle?': 'Estilo_Vida',
        'Section 5: Personal Preferences\n15. How important is comfort in your clothing choices': 'Importancia_Conforto',
        '16.If you had to choose, would you prefer timeless pieces or trendy items?': 'Estilo_Pecas',
        '17. From scale 1-10 how much do you think your clothing style reflects about your personality?': 'Nota_Reflexo'
    }
    df.rename(columns=mapeamento_colunas, inplace=True)

    # Eliminando colunas puramente nulas
    colunas_nulas = [col for col in df_raw.columns if df_raw[col].isnull().all()]
    df.drop(columns=colunas_nulas, errors='ignore', inplace=True)

    # 2. Dicionários para tradução de variáveis qualitativas (Inglês -> Português)
    translations_map = {
        'Genero': {'Female': 'Feminino', 'Male': 'Masculino'},
        'Estilo_Diario': {
            'Chic (e.g., tailored, stylish)': 'Chique/Elegante', 
            'Casual (e.g., jeans, t-shirts)': 'Casual (Jeans/Camiseta)', 
            'Sporty (e.g., activewear, sneakers)': 'Esportivo', 
            'Vintage/Retro': 'Vintage/Retrô', 
            'Bohemian/Boho': 'Boêmio/Boho'
        },
        'Paleta_Cores': {
            'Dark tones (navy, maroon)': 'Tons Escuros (Azul Marinho, Vinho)', 
            'Neutral (black, white, beige)': 'Tons Neutros (Preto, Branco, Bege)', 
            'Pastels (soft pink, baby blue)': 'Tons Pastéis (Rosa Claro, Azul Bebê)', 
            'Bright & Bold (neon, primary colors)': 'Cores Vivas (Neon, Primárias)', 
            'Mixed or patterned': 'Misturado ou Estampado'
        },
        'Prioridade_Uso': {
            'Slightly prefer aesthetics': 'Prefiro Estética', 
            'Slightly prefer functionality': 'Prefiro Funcionalidade', 
            'Equal balance of both': 'Equilíbrio Estética/Funcionalidade'
        },
        'Tipo_Guarda_Roupa': {
            'Mix-and-match (varied styles)': 'Mix-and-Match (Estilos Variados)', 
            'Minimalist (few versatile pieces)': 'Minimalista (Peças Versáteis)', 
            'Specialized (specific to one style)': 'Especializado (Estilo Único)'
        },
        'Frequencia_Compras': {
            'Rarely': 'Raramente', 
            'Every few months': 'A Cada Poucos Meses', 
            'Monthly': 'Mensalmente', 
            'Weekly': 'Semanalmente', 
            'Daily': 'Diariamente'
        },
        'Influencia_Compra': {
            'Comfort': 'Conforto', 
            'Sustainability': 'Sustentabilidade', 
            'Brand reputation': 'Reputação da Marca', 
            'Price': 'Preço', 
            'Trends': 'Tendências'
        },
        'Local_Compras': {
            'Local boutiques': 'Butiques Locais', 
            'Thrift stores': 'Brechós', 
            'Department stores': 'Lojas de Departamento', 
            'Online retailers': 'Varejistas Online', 
            'Fast fashion chains': 'Lojas de Fast Fashion'
        },
        'Eventos_Formais': {
            '- Occasionally (a few times a year)': 'Ocasionalmente (Algumas vezes ao ano)', 
            '- Rarely (less than one once a year)': 'Raramente (Menos de uma vez ao ano)', 
            '- Never': 'Nunca', 
            '- Frequently (several times a year)': 'Frequentemente (Várias vezes ao ano)'
        },
        'Experimenta_Estilos': {
            'Sometimes experiment': 'Às Vezes Experimento', 
            'Rarely experiment': 'Raramente Experimento', 
            'Often experiment': 'Frequentemente Experimento'
        },
        'Tipo_Calcado': {
            'Sneakers': 'Tênis', 
            'Sandals/Flats': 'Sandálias/Sapatilhas', 
            'Boots': 'Botas', 
            'Heels': 'Saltos', 
            'Formal shoes': 'Sapatos Formais'
        },
        'Estilo_Vida': {
            'Mostly sedentary': 'Maioritariamente Sedentário', 
            'Moderadamente active': 'Moderadamente Ativo', 
            'Very active (e.g., gym, outdoor activities)': 'Muito Ativo (Ex: Academia, Atividades ao ar livre)'
        },
        'Importancia_Conforto': {
            'Very important (top priority)': 'Muito Importante (Prioridade Máxima)', 
            'Moderadamente important': 'Moderadamente Importante', 
            'Slightly important': 'Pouco Importante', 
            'Not important': 'Não Importante'
        },
        'Estilo_Pecas': {
            'Trendy pieces': 'Peças da Moda', 
            'Timeless pieces': 'Peças Atemporais'
        }
    }

    # Aplicação das traduções
    for col, dico in translations_map.items():
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().map(dico).fillna('Não Informado')

    colunas_criticas = ['Idade', 'Genero', 'Estilo_Diario', 'Paleta_Cores']
    for col in colunas_criticas:
        if col in df.columns:
            df = df[df[col] != 'Não Informado']

    if 'Nota_Reflexo' in df.columns:
        df.dropna(subset=['Nota_Reflexo'], inplace=True)
        df['Nota_Reflexo'] = pd.to_numeric(df['Nota_Reflexo'], errors='coerce')

    df.reset_index(drop=True, inplace=True)

    # Engenharia de Atributos Derivados
    df["Nivel_Reflexo"] = np.select(
        [df["Nota_Reflexo"] >= 8, df["Nota_Reflexo"] < 5], 
        ["Alto", "Baixo"], 
        default="Médio"
    )
    df["Tipo_Estilo"] = df["Estilo_Diario"].apply(lambda x: "Elegante" if "Chique" in str(x) else "Casual")
    df["Categoria_Cor"] = np.select(
        [df["Paleta_Cores"].str.contains("Pastéis"), df["Paleta_Cores"].str.contains("Escuros"), df["Paleta_Cores"].str.contains("Neutros")], 
        ["Pastel", "Escura", "Neutra"], 
        default="Outros"
    )
    df["Faixa_Consumo"] = np.where(df["Nota_Reflexo"] >= 8, "Premium", "Padrão")
    df["Codigo_Genero"] = df["Genero"].astype("category").cat.codes
    df["Codigo_Estilo"] = df["Estilo_Diario"].astype("category").cat.codes
    df["Indice_Moda"] = (df["Nota_Reflexo"] * 10 + df["Codigo_Genero"] + df["Codigo_Estilo"])

    cols_para_remover = [col for col in df.columns if (df[col] == 'Não Informado').all()]
    df.drop(columns=cols_para_remover, errors='ignore', inplace=True)

    return df

# ==============================================================================
# 3. NAVEGAÇÃO NA BARRA LATERAL
# ==============================================================================
st.sidebar.title("📌 Navegação do Projeto")
pagina = st.sidebar.radio("Ir para:", ["🏠 Home (Apresentação)", "📊 Dashboard Interativo"])

# ==============================================================================
# PÁGINA 1: HOME / APRESENTAÇÃO
# ==============================================================================
if pagina == "🏠 Home (Apresentação)":
    st.title("👔 Identidade e Expressão: A Moda Como Espelho da Personalidade")
    st.caption("Projeto desenvolvido para a disciplina de TPAE II - UFPB")
    
    st.divider()
    
    st.header("🎯 Sobre o Projeto")
    st.write("""
    A moda constitui uma importante forma de comunicação não verbal, desempenhando um papel 
    significativo na construção da identidade e na expressão da personalidade. Mais do que 
    atender à necessidade básica de vestir, o vestuário permite que os indivíduos expressem 
    valores, comportamentos e sentimento de pertencimento social.
    """)
    
    st.header("📌 Problema e Objetivos")
    st.markdown("""
    * **Problema de Pesquisa:** De que maneira as escolhas de vestuário, no cenário contemporâneo, expressam os traços de personalidade dos indivíduos?
    * **Objetivo Geral:** Analisar como a moda atua como forma de expressão da identidade e espelho da personalidade, investigando como as escolhas de vestuário refletem características individuais no público jovem.
    """)
    
    st.divider()
    
    st.header("📁 Descrição dos Dados (Dataset)")
    st.write("""
    Os dados utilizados nesta pesquisa foram obtidos via plataforma **Kaggle**, reunindo informações 
    sobre preferências de estilo, hábitos de consumo e características comportamentais.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Origem dos Dados", "Kaggle")
    col2.metric("Tratamento de Dados", "Python (Pandas)")
    col3.metric("Foco da Amostra", "Público Jovem")

# ==============================================================================
# PÁGINA 2: DASHBOARD INTERATIVO E ANÁLISES
# ==============================================================================
elif pagina == "📊 Dashboard Interativo":
    
    # Carregamento do Dataset
    st.sidebar.divider()
    st.sidebar.subheader("🛠️ Configurações & Filtros")
    arquivo_upload = st.sidebar.file_uploader("Upload do dataset (CSV)", type=["csv"])

    if arquivo_upload is not None:
        df_dados = carregar_e_tratar_dados(arquivo_upload)
    else:
        try:
            # Nome padrão do arquivo no repositório
            df_dados = carregar_e_tratar_dados("Fashion(Data Points) - Form responses 1.csv")
        except Exception:
            st.error("Por favor, faça o upload do arquivo CSV do projeto na barra lateral para carregar os gráficos.")
            st.stop()

    # Filtros Dinâmicos
    generos_disponiveis = df_dados['Genero'].unique().tolist()
    estilos_disponiveis = df_dados['Estilo_Diario'].unique().tolist()

    generos_selecionados = st.sidebar.multiselect(
        "Filtrar por Gênero:",
        options=generos_disponiveis,
        default=generos_disponiveis
    )

    estilos_selecionados = st.sidebar.multiselect(
        "Filtrar por Estilo Diário:",
        options=estilos_disponiveis,
        default=estilos_disponiveis
    )

    df_filtrado = df_dados[
        (df_dados['Genero'].isin(generos_selecionados)) &
        (df_dados['Estilo_Diario'].isin(estilos_selecionados))
    ]

    # Cabeçalho do Dashboard
    st.title("📊 Painel de Análise Visual de Dados")
    st.markdown("Explore os dados quantitativos da pesquisa através das abas temáticas abaixo:")
    st.divider()

    # Abas Temáticas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visão Geral Descritiva", 
        "🎨 Estilos & Preferências", 
        "🧠 Percepção & Personalidade", 
        "📋 Base Tratada (ETL)"
    ])

    # ABA 1: VISÃO GERAL
    with tab1:
        st.header("Resumo Estatístico Descritivo (Seção 4.3)")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Respostas Analisadas", f"{len(df_filtrado)}")
        col2.metric("Média Nota do Reflexo", f"{df_filtrado['Nota_Reflexo'].mean():.2f} / 10" if not df_filtrado.empty else "N/A")
        col3.metric("Estilo Predominante", df_filtrado['Estilo_Diario'].mode()[0] if not df_filtrado.empty else "N/A")
        col4.metric("Índice Sintético de Moda", f"{df_filtrado['Indice_Moda'].mean():.1f}" if not df_filtrado.empty else "N/A")
        
        st.divider()
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.subheader("Distribuição da Amostra por Gênero")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df_filtrado, x='Genero', palette='Set2', ax=ax)
            ax.set_xlabel("Gênero")
            ax.set_ylabel("Frequência Absoluta")
            st.pyplot(fig)

        with col_g2:
            st.subheader("Categorização do Nível de Reflexo da Personalidade")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df_filtrado, x='Nivel_Reflexo', order=['Baixo', 'Médio', 'Alto'], palette='Blues_r', ax=ax)
            ax.set_xlabel("Nível do Reflexo")
            ax.set_ylabel("Frequência Absoluta")
            st.pyplot(fig)

    # ABA 2: ESTILOS & PREFERÊNCIAS
    with tab2:
        st.header("Análise de Preferências Estéticas e Hábitos")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            st.subheader("Paletas de Cores Mais Frequentadas")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df_filtrado, y='Paleta_Cores', palette='mako', ax=ax)
            ax.set_xlabel("Quantidade")
            ax.set_ylabel("Paleta de Cores")
            st.pyplot(fig)

        with col_e2:
            st.subheader("Prioridade de Uso (Estética vs. Funcionalidade)")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df_filtrado, y='Prioridade_Uso', palette='rocket', ax=ax)
            ax.set_xlabel("Quantidade")
            ax.set_ylabel("Prioridade")
            st.pyplot(fig)

    # ABA 3: PERCEPÇÃO & PERSONALIDADE
    with tab3:
        st.header("Interseção entre Estilos Diários e Nota do Reflexo")
        
        st.markdown("""
        O gráfico de caixa (*boxplot*) abaixo apresenta a distribuição empírica das avaliações sobre o quanto o vestuário 
        reflete a personalidade (em escala de 1 a 10) segmentada pelos estilos de roupa cotidianos.
        """)
        
        fig, ax = plt.subplots(figsize=(9, 4.5))
        sns.boxplot(data=df_filtrado, x='Estilo_Diario', y='Nota_Reflexo', palette='viridis', ax=ax)
        ax.set_title("Percepção do Reflexo da Personalidade por Categoria de Estilo")
        ax.set_xlabel("Estilo Diário")
        ax.set_ylabel("Nota do Reflexo (1 a 10)")
        st.pyplot(fig)

    # ABA 4: BASE TRATADA
    with tab4:
        st.header("Base de Dados Processada e Enriquecida")
        st.markdown("Abaixo encontra-se a tabela após as etapas de tradução, limpeza de nulos e engenharia de variáveis:")
        
        st.dataframe(df_filtrado, use_container_width=True)
        
        csv_dados = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados Tratados em CSV",
            data=csv_dados,
            file_name='dados_moda_tratados.csv',
            mime='text/csv'
        )
st.divider()

st.subheader("Conclusão")

st.write("""
O presente estudo analisou a relação entre moda, identidade e comportamento de consumo utilizando dados da plataforma Kaggle e técnicas de análise em Python. Os resultados demonstraram que o vestuário desempenha um papel importante na construção da identidade, sendo utilizado não apenas para atender necessidades funcionais, mas também como forma de expressar personalidade, valores e estilo de vida.

As análises evidenciaram que os participantes procuram equilibrar estética e funcionalidade em suas escolhas de vestuário, indicando que o processo de decisão de compra envolve fatores práticos e simbólicos. Além disso, observou-se que a maioria realiza compras de maneira planejada, sugerindo um comportamento de consumo mais consciente.

Também foi identificada a predominância do estilo casual entre os respondentes, refletindo a preferência por peças versáteis e confortáveis para o cotidiano. As diferenças entre os gêneros mostraram-se pouco significativas, indicando padrões de consumo semelhantes na amostra analisada.

Por fim, conclui-se que a utilização de ferramentas como Python, Pandas, Matplotlib e Streamlit permitiu transformar dados em informações relevantes para compreender o comportamento do consumidor de moda. A integração entre ciência de dados e estudos de moda mostrou-se eficiente para apoiar análises quantitativas e ampliar a compreensão sobre identidade e consumo.
""")
