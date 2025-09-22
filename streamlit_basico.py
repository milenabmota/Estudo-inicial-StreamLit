import streamlit as st
import pandas as pd
import plotly.express as px

##Título da pagina
st.set_page_config(page_title="Explorador de Expectativa de Vida", layout="wide")

## Título da página
st.title("Gapminder - Explorador de Expectativa de Vida")

st.markdown("Filtre por ano e continente para explorar a expectativa de vida ao longo do tempo.")

# Carregar os dados
@st.cache_data
def load_data():
    #Carregar dados do Plotly Express
    return px.data.gapminder()

#Os dados são carregados em uma variável chamada "df" ao chamar a função load_data()
df = load_data()

#Cria um sidebar para os filtros 
st.sidebar.header("Filtros")
#Cria um filtro deslizante para selecionar o ano
#O valor inicial é 2007, que é o último ano disponível no conjunto de dados
year = st.sidebar.slider("Ano", int(df.year.min()), int(df.year.max()), 2007)

#Cria um filtro de múltipla seleção para selecionar os continentes
continents = st.sidebar.multiselect("Continente", options=df.continent.unique(), default=df.continent.unique())

#Filtra os dados com base no ano e nos continentes selecionados
df_filt = df[(df.year == year) & (df.continent.isin(continents))]

#Criar três colunas para exibir as métricas lado a lado
col1, col2, col3 = st.columns(3)
#Número de registros (linhas) no DataFrame filtrado
col1.metric("Registros", len(df_filt))
#Exibe a expectativa de vida mínima, formatada com uma casa decimal
col2.metric("Mín Vida", f"{df_filt.lifeExp.min():.1f}")
#Exibe a expectativa de vida máxima, formatada com uma casa decimal
col3.metric("Máx Vida", f"{df_filt.lifeExp.max():.1f}")

st.markdown("---")


#Cria duas colunas para orrganizar o layout
left, right = st.columns(2)

with left:
    st.subheader("Dados")
    st.dataframe(
        df_filt.rename(columns={
            "country": "País",
            "continent": "Continente",
            "year": "Ano",
            "lifeExp": "Expectativa de Vida",
            "pop": "População",
            "gdpPercap": "PIB per Capita",
            "iso_alpha": "ISO Alpha",
            "iso_num": "ISO Numérico"
        }).reset_index(drop=True), 
        use_container_width=True
    )

with right:
    st.subheader("Expectativa de Vida vs PIB per Capita")
    fig = px.scatter(
        df_filt,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
        title=f"{year} - Expectativa de Vida vs PIB per Capita",
    )
    st.plotly_chart(fig, use_container_width=True)


##https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
##https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account
##streamlit run streamlit_basico.py
