import streamlit as st
import pandas as pd
import plotly.express as px

#Configuração da Página
st.set_page_config(page_title="Dashboard de Energia", layout="wide")
st.title("⚡ Produção de Energia no Brasil (2015-2024)")
st.markdown("Análise da evolução da produção energética, identificando fontes predominantes, consumo e impactos ambientais.")

# 2. Carregar os Dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/simulacao_producao_energia_brasil.csv')
    df['data'] = pd.to_datetime(df['data'])
    return df

df = carregar_dados()

#Filtros
st.sidebar.header("Filtros Analíticos")
anos_selecionados = st.sidebar.multiselect("Ano", sorted(df['ano'].unique()))
regioes_selecionadas = st.sidebar.multiselect("Região", sorted(df['regiao'].unique()))
fontes_selecionadas = st.sidebar.multiselect("Fonte Energética", sorted(df['fonte_energia'].unique()))

#filtragem dinâmica
df_filtrado = df.copy()
if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
if regioes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['regiao'].isin(regioes_selecionadas)]
if fontes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['fonte_energia'].isin(fontes_selecionadas)]

#KPI
st.subheader("Indicadores Principais")

if not df_filtrado.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Produção Total", f"{df_filtrado['producao_mwh'].sum():,.0f} MWh")
    
    fonte_max = df_filtrado.groupby('fonte_energia')['producao_mwh'].sum().idxmax()
    col2.metric("Fonte Predominante", fonte_max)
    
    estado_max = df_filtrado.groupby('uf')['producao_mwh'].sum().idxmax()
    col3.metric("Estado Líder de Produção", estado_max)
    
    col4.metric("Consumo Total", f"{df_filtrado['consumo_mwh'].sum():,.0f} MWh")
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

#Visualizações
st.subheader("Análises Visuais")
tab1, tab2 = st.tabs(["Evolução e Matriz", "Análise Regional"])

with tab1:
    # Gráfico de Linha Temporal
    evolucao = df_filtrado.groupby('data')['producao_mwh'].sum().reset_index()
    fig_linha = px.line(evolucao, x='data', y='producao_mwh', title="Evolução Temporal da Produção")
    st.plotly_chart(fig_linha, use_container_width=True)

    # Gráfico de Pizza da Matriz
    matriz = df_filtrado.groupby('fonte_energia')['producao_mwh'].sum().reset_index()
    fig_pizza = px.pie(matriz, names='fonte_energia', values='producao_mwh', title="Participação na Matriz Energética")
    st.plotly_chart(fig_pizza, use_container_width=True)

with tab2:
    # Gráfico de Barras por Estado
    prod_estado = df_filtrado.groupby('uf')['producao_mwh'].sum().reset_index()
    fig_barras = px.bar(prod_estado, x='uf', y='producao_mwh', title="Produção por Estado")
    st.plotly_chart(fig_barras, use_container_width=True)


st.subheader("Conclusão Executiva")
st.markdown("Através das análises, observa-se a diversidade da matriz energética brasileira e o impacto de diferentes fontes na sustentabilidade e desenvolvimento regional.")