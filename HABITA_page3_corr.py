import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import os
from streamlit_option_menu import option_menu

################################################################
#run: streamlit run "dashboard\pages\HABITA_page3_corr.py"
#os.chdir(os.path.join(os.getcwd(), "dashboard")) #Alterar o diretório de trabalho para 'dashboard'
#print("Current working directory:", os.getcwd()) 
################################################################

# Configuração da página
st.set_page_config(page_title="Mapa de Clusters", layout="wide")
########################################################################

@st.cache_data
def load_data():
    gdf_CONC = gpd.read_file("cc98.shp")
    df_2011 = pd.read_csv("indicadores_2011.csv", encoding="ISO-8859-1")
    df_2021 = pd.read_csv("indicadores_2021.csv", encoding="ISO-8859-1")
    df_variacao = pd.read_csv("indicadores_2011_2021.csv", encoding="ISO-8859-1")

    df_2011["GEOID"] = df_2011["GEOID"].fillna("0000").astype(str).str.zfill(4)
    df_2021["GEOID"] = df_2021["GEOID"].fillna("0000").astype(str).str.zfill(4)
    df_variacao["GEOID"] = df_variacao["GEOID"].fillna("0000").astype(str).str.zfill(4)

    gdf2011 = gdf_CONC.merge(df_2011, how="left", left_on="GEOID", right_on="GEOID")
    gdf2021 = gdf_CONC.merge(df_2021, how="left", left_on="GEOID", right_on="GEOID")
    gdf_variacao = gdf_CONC.merge(df_variacao, how="left", left_on="GEOID", right_on="GEOID")

    return gdf_CONC, gdf2011, gdf2021, gdf_variacao

# Captura gdf_CONC além dos outros DataFrames
gdf_CONC, gdf2011, gdf2021, gdf_variacao = load_data()

#######################################################################
# Menu lateral
with st.sidebar:
    # Configurações de Ano e Indicadores
    st.header("Indicadores para a análise")
    
    # Seleção de ano
    ano = st.selectbox("Selecione o ano", ["2011", "2021", "Variação"], index=1)

    # Definição de indicadores com base no ano
    if ano == "2011":
        gdf = gdf2011
        indicadores = [col for col in gdf.columns if "2011" in col]
    elif ano == "2021":
        gdf = gdf2021
        indicadores = [col for col in gdf.columns if "2021" in col]
    else:
        gdf = gdf_variacao
        indicadores = [col for col in gdf.columns if "2011_2021" in col]

    # Seleção de indicadores
    indicador_x = st.selectbox("Selecione o primeiro indicador (X)", indicadores, key="x")
    indicador_y = st.selectbox("Selecione o segundo indicador (Y)", indicadores, key="y")


if indicador_x and indicador_y:
    data = gdf[["geometry", indicador_x, indicador_y]].dropna()
    data.columns = ["geometry", "indicador_x", "indicador_y"]

    # Calcule a mediana
    median_x = data["indicador_x"].median()
    median_y = data["indicador_y"].median()

    # Clusterização
    data["Cluster"] = np.where(
        (data["indicador_x"] > median_x) & (data["indicador_y"] > median_y), 1,
        np.where(
            (data["indicador_x"] > median_x) & (data["indicador_y"] <= median_y), 2,
            np.where(
                (data["indicador_x"] <= median_x) & (data["indicador_y"] > median_y), 3,
                4
            )
        )
    )
    # Definição de cores e rótulos dos clusters
    cluster_colors = ['#bfcfbe', '#639917', '#497fa6', '#f2eb8d']
    cluster_labels = ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"]
    
    # Títulos dinâmicos para os eixos
    x_label = indicador_x.replace("_", " ").title()
    y_label = indicador_y.replace("_", " ").title()

    # Criação do layout de colunas
    col1, col2 = st.columns([3, 4])

        # Mapa na coluna 1
    with col1:
        #st.subheader("Mapa de Clusters")
        gdf_cluster = gpd.GeoDataFrame(data, geometry="geometry")
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        legend_dict = {}
        for cluster, color in enumerate(cluster_colors, start=1):
            gdf_cluster[gdf_cluster["Cluster"] == cluster].plot(
                ax=ax, color=color, edgecolor="black", linewidth=0.2
            )
            legend_dict[f"Cluster {cluster}"] = color

        #ax.set_title("Clusters no Mapa")
        ax.axis("off")
        st.pyplot(fig)

# Scatterplot na coluna 2
with col2:
    #st.subheader("Dispersão e Correlação de Indicadores")
    fig, ax = plt.subplots(figsize=(6, 6))
    for cluster, group in data.groupby("Cluster"):
        ax.scatter(
            group["indicador_x"], group["indicador_y"],
            label=f"{cluster_labels[cluster-1]}",
            color=cluster_colors[cluster-1],
            alpha=0.7
        )

    # Calcular a correlação
    correlation = data["indicador_x"].corr(data["indicador_y"])

    # Adicionar linhas de medianas com rótulos
    ax.axhline(median_y, color="#639917", linestyle="--", label=f"Mediana {y_label}: {median_y:.2f}")
    ax.axvline(median_x, color="orange", linestyle="--", label=f"Mediana {x_label}: {median_x:.2f}")

    # Adicionar título dinâmico com correlação personalizada
    ax.text(
        0.5, 1.1,  # Coordenadas relativas ao eixo
        f"Relação entre {x_label} e {y_label}",  # Primeira linha
        fontsize=14, color='black', weight='normal', ha='center', transform=ax.transAxes
    )
    ax.text(
        0.5, 1.02,  # Coordenadas para a segunda linha
        f"(Correlação: {correlation:.2f})",  # Segunda linha
        fontsize=12, color='grey', weight='bold', ha='center', transform=ax.transAxes
    )

    # Definir rótulos dos eixos
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Remover as linhas de cima e do lado direito
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Exibir o gráfico antes de usar o st.pyplot
    st.pyplot(fig)


    # Legenda combinada
    st.markdown("<style>h3 { margin-bottom: -20x; }</style>", unsafe_allow_html=True)  # Reduz espaço entre título e legenda
    #st.subheader("Legenda")
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis("off")  # Remove o fundo do gráfico

    # Adicionar os clusters à legenda
    for cluster, color in enumerate(cluster_colors, start=1):
        ax.scatter([], [], c=color, label=f"{cluster_labels[cluster-1]}", s=100)

    # Adicionar as linhas de mediana à legenda
    ax.plot([], [], color="orange", linestyle="--", label=f"Mediana {y_label}: {median_y:.2f}")
    ax.plot([], [], color="#639917", linestyle="--", label=f"Mediana {x_label}: {median_x:.2f}")

    ax.legend(loc="center", bbox_to_anchor=(0.5, 1.2),  ncol=3, frameon=False)  # Configuração centralizada
    st.pyplot(fig)
