################################################################
#run: streamlit run "dashboard\pages\HABITA_page4_idesig.py"
#os.chdir(os.path.join(os.getcwd(), "dashboard")) #Alterar o diretório de trabalho para 'dashboard'
#print("Current working directory:", os.getcwd()) 
################################################################

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import os
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

################################################################
st.set_page_config(
    page_title="Portal HABITA - Indicadores de Desigualdade", layout="wide")
################################################################

# Função para carregar os dados
@st.cache_data
def load_data():
    # Carregar dados
    df_id = pd.read_csv("indices_desigualdades.csv", encoding="ISO-8859-1")
    df_id_2011_2021 = pd.read_csv("indices_desigualdades_2011_2021.csv", encoding="ISO-8859-1")
    return df_id, df_id_2011_2021

# Carregar dados
df_id, df_id_2011_2021 = load_data()


################################################################

# Configuração do menu lateral
st.sidebar.header("Configurações")
indicador_selecionado = st.sidebar.selectbox("Selecione o indicador", df_id['Indicador'].unique())

################################################################

# Obter os valores dos índices para 2011 e 2021
try:
    indice_moran_2011 = df_id.loc[df_id['Indicador'] == indicador_selecionado, 'Índice de Moran'].values[0]
    indice_gini_2011 = df_id.loc[df_id['Indicador'] == indicador_selecionado, 'Indice de Gini'].values[0]

    # Obter valores para 2021
    indice_moran_2021 = df_id.loc[df_id['Indicador'] == indicador_selecionado.replace("_2011", "_2021"), 'Índice de Moran'].values[0]
    indice_gini_2021 = df_id.loc[df_id['Indicador'] == indicador_selecionado.replace("_2011", "_2021"), 'Indice de Gini'].values[0]
except IndexError:
    indice_moran_2011, indice_gini_2011, indice_moran_2021, indice_gini_2021 = None, None, None, None

################################

# Evolução dos Índices
st.markdown("<h2 style='font-size: 18px; color: #46494d;'>Evolução dos Índices de Desigualdade</h2>", unsafe_allow_html=True)

if indice_moran_2011 is not None and indice_moran_2021 is not None:
    # Cálculo da evolução
    var_moran_abs = indice_moran_2021 - indice_moran_2011
    var_gini_abs = indice_gini_2021 - indice_gini_2011

    var_moran_perc = (var_moran_abs / indice_moran_2011) * 100
    var_gini_perc = (var_gini_abs / indice_gini_2011) * 100

    # Exibição dos valores em duas colunas
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Índice de Moran (Evolução)", value=f"{indice_moran_2021:.3f}", delta=f"{var_moran_abs:.3f} ({var_moran_perc:.2f}%)")
    with col2:
        st.metric(label="Índice de Gini (Evolução)", value=f"{indice_gini_2021:.3f}", delta=f"{var_gini_abs:.3f} ({var_gini_perc:.2f}%)")

    # Gráfico Comparativo
    fig = go.Figure()

    # Adicionar barras para 2011
    fig.add_trace(go.Bar(
        x=["Índice de Moran", "Índice de Gini"],
        y=[indice_moran_2011, indice_gini_2011],
        name="2011",
        marker_color="darkblue"
    ))

    # Adicionar barras para 2021
    fig.add_trace(go.Bar(
        x=["Índice de Moran", "Índice de Gini"],
        y=[indice_moran_2021, indice_gini_2021],
        name="2021",
        marker_color="grey"
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        barmode="group",
        xaxis_title="Índices",
        yaxis_title="Valores",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Os índices para 2011 e 2021 não estão disponíveis para o indicador selecionado.")

################################################################
# Divisor 
st.markdown(
    """
    <hr style="border: 1px solid #bdc3c7; margin-top: 20px; margin-bottom: 20px;">
    """,
    unsafe_allow_html=True,
)
################################################################
# Função para criar gráficos 
def plot_top_bottom(data, column, title, xlabel):
    # Obter Top 5 e Bottom 5
    top_5 = data.nlargest(5, column)
    bottom_5 = data.nsmallest(5, column)
    combined = pd.concat([top_5, bottom_5])

    # Configuração do gráfico
    plt.figure(figsize=(8, 8))  # Aumentei o tamanho do gráfico
    sns.barplot(
        y="Indicador",
        x=column,
        data=combined,
        palette="cividis",  
        order=combined.sort_values(column, ascending=False)["Indicador"]
    )
    sns.despine()  # Remove as bordas do gráfico
    plt.title(title, fontsize=10, pad=20)  # Título maior e com espaçamento
    plt.xlabel(xlabel, fontsize=14)  # Fonte maior no eixo X
    plt.ylabel("", fontsize=20)  # Fonte ajustada no eixo Y
    plt.xticks(fontsize=12)  # Aumentar fonte dos valores do eixo X
    plt.yticks(fontsize=14)  # Aumentar fonte do eixo Y
    for index, value in enumerate(combined[column]):
        plt.text(value, index, f"{value:.3f}", va="center", ha="left", fontsize=12)  # Anotações maiores
    return plt

# Exibir gráficos em 3 colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='text-align: center; font-size:16px;'>Top 5 e Bottom 5 do Índice de Gini 2011</h3>", unsafe_allow_html=True)  # Alterando o tamanho do título
    plot1 = plot_top_bottom(df_id_2011_2021, "Indice de Gini_2011", "Top 5 e Bottom 5 - Índice de Gini 2011", "Índice de Gini 2011")
    st.pyplot(plot1)

with col2:
    st.markdown("<h3 style='text-align: center; font-size:16px;'>Top 5 e Bottom 5 do Índice de Gini 2021</h3>", unsafe_allow_html=True)  # Alterando o tamanho do título
    plot2 = plot_top_bottom(df_id_2011_2021, "Indice de Gini_2021", "Top 5 e Bottom 5 - Índice de Gini 2021", "Índice de Gini 2021")
    st.pyplot(plot2)

with col3:
    st.markdown("<h3 style='text-align: center; font-size:16px;'>Top 5 e Bottom 5 da Variação do Índice de Gini</h3>", unsafe_allow_html=True)  # Alterando o tamanho do título
    plot3 = plot_top_bottom(df_id_2011_2021, "Gini_var_abs", "Top 5 e Bottom 5 - Variação Absoluta", "Variação Absoluta do Índice de Gini")
    st.pyplot(plot3)


################################################################
# Divisor 
st.markdown(
    """
    <hr style="border: 1px solid #bdc3c7; margin-top: 20px; margin-bottom: 20px;">
    """,
    unsafe_allow_html=True,
)
################################################################

# Adicionar título principal
st.markdown("<h2 style='text-align: left; font-size:16px; color: #2c3e50;'>Descarregue os Índices de Desigualdade</h2>", unsafe_allow_html=True)


# Criar abas para os anos
tab1, tab2 = st.tabs(["2011", "2021"])

# Filtrar os dados por ano e selecionar apenas as colunas necessárias
df_2011 = df_id[df_id["Ano"] == 2011][["Indicador", "Índice de Moran", "Indice de Gini"]]
df_2021 = df_id[df_id["Ano"] == 2021][["Indicador", "Índice de Moran", "Indice de Gini"]]

# Tabela de 2011
with tab1:
    st.markdown("<h3 style='text-align: center; color: #46494d;'>Dados de 2011</h3>", unsafe_allow_html=True)
    st.dataframe(df_2011)  # Exibir tabela de 2011
    # Criar CSV para download
    csv_2011 = df_2011.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar Dados de 2011",
        data=csv_2011,
        file_name="dados_2011.csv",
        mime="text/csv"
    )

# Tabela de 2021
with tab2:
    st.markdown("<h3 style='text-align: center; color: #46494d;'>Dados de 2021</h3>", unsafe_allow_html=True)
    st.dataframe(df_2021)  # Exibir tabela de 2021
    # Criar CSV para download
    csv_2021 = df_2021.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar Dados de 2021",
        data=csv_2021,
        file_name="dados_2021.csv",
        mime="text/csv"
    )
################################################################