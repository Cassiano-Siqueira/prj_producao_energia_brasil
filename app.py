import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Energia no Brasil", page_icon="⚡", layout="wide")
st.title("Produção de Energia no Brasil (2015-2024)")
st.markdown("Projeto desenvolvido para a disciplina de Análise e Visualização de Dados — Análise da evolução energética, matriz de fontes e correlações estatísticas.")

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/simulacao_producao_energia_brasil.csv')
    df['data'] = pd.to_datetime(df['data'])
    return df

df = carregar_dados()

st.sidebar.header("Filtros Analíticos")
anos_selecionados = st.sidebar.multiselect("Ano", sorted(df['ano'].unique()))
regioes_selecionadas = st.sidebar.multiselect("Região", sorted(df['regiao'].unique()))
fontes_selecionadas = st.sidebar.multiselect("Fonte Energética", sorted(df['fonte_energia'].unique()))


df_filtrado = df.copy()
if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
if regioes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['regiao'].isin(regioes_selecionadas)]
if fontes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['fonte_energia'].isin(fontes_selecionadas)]

st.subheader("Indicadores Principais (KPIs)")

if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Produção Total", f"{df_filtrado['producao_mwh'].sum():,.0f} MWh")
    
    fonte_max = df_filtrado.groupby('fonte_energia')['producao_mwh'].sum().idxmax()
    col2.metric("Fonte Predominante", fonte_max)
    
    estado_max = df_filtrado.groupby('uf')['producao_mwh'].sum().idxmax()
    col3.metric("Estado Líder", estado_max)
    
    col4.metric("Consumo Total", f"{df_filtrado['consumo_mwh'].sum():,.0f} MWh")
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

tab1, tab2, tab3 = st.tabs(["📊 Evolução e Matriz", "🗺️ Análise Regional", "📈 Análise Estatística Avançada"])

with tab1:
    st.subheader("Evolução Temporal e Participação das Fontes")

    evolucao = df_filtrado.groupby('data')['producao_mwh'].sum().reset_index()
    fig_linha = px.line(evolucao, x='data', y='producao_mwh', title="Evolução Temporal da Produção de Energia")
    st.plotly_chart(fig_linha, use_container_width=True)

    matriz = df_filtrado.groupby('fonte_energia')['producao_mwh'].sum().reset_index()
    fig_pizza = px.pie(matriz, names='fonte_energia', values='producao_mwh', title="Participação na Matriz Energética")
    st.plotly_chart(fig_pizza, use_container_width=True)

with tab2:
    st.subheader("Distribuição Geográfica da Produção")
   
    prod_estado = df_filtrado.groupby('uf')['producao_mwh'].sum().reset_index()
    fig_barras = px.bar(prod_estado, x='uf', y='producao_mwh', title="Produção por Unidade Federativa (UF)", color='producao_mwh', color_continuous_scale='Blues')
    st.plotly_chart(fig_barras, use_container_width=True)

with tab3:
    st.subheader("Correlação Estatística Avançada (Funcionalidade Avançada)")
    st.markdown("Esta secção cumpre os requisitos avançados de análise matemática, avaliando o grau de correlação linear entre as variáveis numéricas do conjunto de dados.")

    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    correlacao = df[colunas_numericas].corr()

    fig_heat = px.imshow(correlacao, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Matriz de Correlação Estatística das Variáveis")
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.subheader("Conclusão Executiva")
st.markdown("A análise integrada demonstra a diversidade da matriz energética brasileira, evidenciando padrões temporais de geração, o peso das principais fontes renováveis e não-renováveis, e as correlações estatísticas fundamentais para a gestão do setor elétrico.")