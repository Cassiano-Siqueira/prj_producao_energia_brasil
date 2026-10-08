import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Energia no Brasil", layout="wide")
st.title("Produção de Energia no Brasil (2015-2024)")
st.markdown("Projeto desenvolvido para a disciplina de Análise e Visualização de Dados — Análise da evolução energética, matriz de fontes e análises comparativas avançadas.")

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
s
tab1, tab2, tab3 = st.tabs(["Evolucao e Matriz", "Analise Regional", "Analise Avancada de Fontes"])

with tab1:
    st.subheader("Evolucao Temporal e Participacao das Fontes")
    evolucao = df_filtrado.groupby('data')['producao_mwh'].sum().reset_index()
    fig_linha = px.line(evolucao, x='data', y='producao_mwh', title="Evolucao Temporal da Producao de Energia")
    st.plotly_chart(fig_linha, use_container_width=True)
    matriz = df_filtrado.groupby('fonte_energia')['producao_mwh'].sum().reset_index()
    fig_pizza = px.pie(matriz, names='fonte_energia', values='producao_mwh', title="Participacao na Matriz Energetica")
    st.plotly_chart(fig_pizza, use_container_width=True)

with tab2:
    st.subheader("Distribuicao Geografica da Producao")
    prod_estado = df_filtrado.groupby('uf')['producao_mwh'].sum().reset_index()
    fig_barras = px.bar(prod_estado, x='uf', y='producao_mwh', title="Producao por Unidade Federativa (UF)", color='producao_mwh', color_continuous_scale='Blues')
    st.plotly_chart(fig_barras, use_container_width=True)

with tab3:
    st.subheader("Comparativo Avançado entre Fontes de Energia")
    st.markdown("Esta ferramenta avançada permite comparar o comportamento de duas fontes energéticas distintas com base na produção e capacidade instalada.")
    lista_fontes = sorted(df['fonte_energia'].unique())
    if len(lista_fontes) >= 2:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fonte_a = st.selectbox("Selecione a Primeira Fonte", lista_fontes, index=0)
        with col_f2:
            fonte_b = st.selectbox("Selecione a Segunda Fonte", lista_fontes, index=1 if len(lista_fontes) > 1 else 0)
        df_comp = df[df['fonte_energia'].isin([fonte_a, fonte_b])]
        comp_agrupado = df_comp.groupby(['ano', 'fonte_energia'])['producao_mwh'].sum().reset_index()
        fig_comp = px.bar(comp_agrupado, x='ano', y='producao_mwh', color='fonte_energia', barmode='group', title=f"Comparativo Anual de Producao: {fonte_a} vs {fonte_b}")
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown("### Estatísticas Descritivas do Comparativo")
        estatisticas = df_comp.groupby('fonte_energia')['producao_mwh'].describe()
        st.dataframe(estatisticas, use_container_width=True)
    else:
        st.info("Dados insuficientes para comparativo.")

st.markdown("---")
st.subheader("Conclusao Executiva")
st.markdown("A analise integrada demonstra a diversidade da matriz energetica brasileira, evidenciando padroes temporais de geracao, o peso das principais fontes renovaveis e nao-renovaveis, e comparativos estatisticos avancados para a gestao do setor eletrico.")


st.sidebar.markdown('<div style="position: fixed; bottom: 20px; width: 250px;"><hr style="border: 0.5px solid #555; margin-bottom: 10px;"><small>Desenvolvido por Cassiano Siqueira<br>Disciplina de Linguagem de Programação<br>Prof: Alexandre Neves Louzada</small></div>', unsafe_allow_html=True)