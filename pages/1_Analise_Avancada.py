import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise Avançada", page_icon="📈", layout="wide")
st.title("📈 Análise Estatística Avançada")
st.markdown("Esta página demonstra funcionalidades avançadas do projeto, isolando a relação estatística entre as variáveis da base de dados.")

@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados/simulacao_producao_energia_brasil.csv')
    return df

df = carregar_dados()

st.subheader("Matriz de Correlação")
st.markdown("A correlação mede como as variáveis numéricas se relacionam (ex: se a produção sobe, o consumo também sobe?). O valor varia de -1 (inverso) a 1 (direto).")

colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
correlacao = df[colunas_numericas].corr()

fig = px.imshow(correlacao, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Heatmap de Correlação Energética")
st.plotly_chart(fig, use_container_width=True)