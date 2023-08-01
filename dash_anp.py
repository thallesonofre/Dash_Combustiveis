import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# configuração da página para wide screem
st.set_page_config(layout="wide")


@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "database_anp.xlsx",
        engine="openpyxl",
        sheet_name="Planilha1",
        usecols="A:Q",
        nrows=19964
    )
    return df
df = gerar_df()
colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    st.subheader("COMPARATIVO DE PREÇOS")
    logo_teste = Image.open('logoP1000.jpg')
    st. image(logo_teste, use_column_width=True)
    st.subheader('SELEÇÃO DE FILTROS')
    fProduto = st.selectbox(
        "Selecione o Combustível:",
        options=df['PRODUTO'].unique()
    )
    
    fEstado = st.selectbox(
        "Selecione o Estado:",
        options=df['ESTADO'].unique()
    )
    
    #Filtrando dados
    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df['ESTADO'] == fEstado)
    ]
    
# formatar o campa da data
updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0:]

# título da página
st.header("PREÇO DOS COMBUSTÍVEIS NO BRASIL: 2013 À 2023")
st.markdown("**Combustível selecionado:** " + fProduto)
st.markdown("**Estado:** " + fEstado)

# gráficos altair
grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x = 'MÊS:T',
    y = 'PREÇO MÉDIO REVENDA',
    strokeWidth = alt.value(3)
).properties(
    height = 400,
    width = 800
)

st.altair_chart(grafCombEstado)