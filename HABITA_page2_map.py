import folium
from branca.colormap import linear
import geopandas as gpd
import plotly.express as px
import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.graph_objects as go
import os

################################################################
#run: streamlit run "dashboard\pages\HABITA_page2_map.py"
#os.chdir(os.path.join(os.getcwd(), "dashboard")) #Alterar o diretório de trabalho para 'dashboard'
#print("Current working directory:", os.getcwd()) 
################################################################


# Configuração da página
st.set_page_config(page_title="Indicadores de Habitação", layout="wide")

# Título e Descritivo no banner
st.title("Indicadores de Habitação em Portugal")
#----------------------------------------------------------------

# Importar dados
@st.cache_data
def load_data():
    gdf_base = gpd.read_file("georef-portugal-concelho.json")
    df_2011 = pd.read_csv("indicadores_2011.csv", encoding="ISO-8859-1")
    df_2021 = pd.read_csv("indicadores_2021.csv", encoding="ISO-8859-1")
    df_variacao = pd.read_csv("indicadores_2011_2021.csv", encoding="ISO-8859-1")
    df_IHRU = pd.read_csv("indicadores_IHRU.csv", encoding="ISO-8859-1")

    df_2011["GEOID"] = df_2011["GEOID"].fillna("0000").astype(str).str.zfill(4)
    df_2021["GEOID"] = df_2021["GEOID"].fillna("0000").astype(str).str.zfill(4)
    df_variacao["GEOID"] = df_variacao["GEOID"].fillna("0000").astype(str).str.zfill(4)
    df_IHRU["GEOID"] = df_IHRU["GEOID"].fillna("0000").astype(str).str.zfill(4)

    gdf2011 = gdf_base.merge(df_2011, how="left", left_on="con_code", right_on="GEOID")
    gdf2021 = gdf_base.merge(df_2021, how="left", left_on="con_code", right_on="GEOID")
    gdf_variacao = gdf_base.merge(df_variacao, how="left", left_on="con_code", right_on="GEOID")
    df_IHRU = gdf_base.merge(df_IHRU, how="left", left_on="con_code", right_on="GEOID")

    return gdf2011, gdf2021, gdf_variacao, df_IHRU

gdf2011, gdf2021, gdf_variacao,df_IHRU = load_data()

################################################################

# Criar seleção no Streamlit
st.sidebar.header("Configurações")
st.sidebar.markdown(
    """
    Utilize as opções abaixo para selecionar o ano e o indicador que deseja visualizar.
    """
)
ano = st.sidebar.selectbox("Selecione o ano", ["2011", "2021", "Variação"], index=1)

if ano == "2011":
    gdf = gdf2011
    indicadores = [
        'Indice_Volumetria_2011', 'Percentagem_Vagos_2011', 'Idade_Media_Edif_2011',
        'Percentagem_Alojamento_Habitual_2011', 'Dimensao_Alojamento_2011',
        'Alojamento_Por_Familia_2011', 'Percentagem_Arrendamento_2011', 'Numero_Divisoes_2011',
        'Indicador_Acessibilidade_Economica_2011'
    ]
elif ano == "2021":
    gdf = gdf2021
    indicadores = [
        'Indice_Volumetria_2021', 'Percentagem_Vagos_2021', 'Idade_Media_Edif_2021',
        'Percentagem_Alojamento_Habitual_2021', 'Dimensao_Alojamento_2021',
        'Alojamento_Por_Familia_2021', 'Percentagem_Arrendamento_2021', 'Numero_Divisoes_2021',
        'Indicador_Acessibilidade_Economica_2021'
    ]
else:
    gdf = gdf_variacao
    indicadores = [
        'Indice_Volumetria_2011_2021', 'Percentagem_Vagos_2011_2021', 'Idade_Media_Edif_2011_2021',
        'Percentagem_Alojamento_Habitual_2011_2021', 'Dimensao_Alojamento_2011_2021',
        'Alojamento_Por_Familia_2011_2021', 'Percentagem_Arrendamento_2011_2021', 'Numero_Divisoes_2011_2021',
        'Indicador_Acessibilidade_Economica_2011_2021'
    ]

indicador_selecionado = st.sidebar.selectbox("Selecione o indicador para caracterização", indicadores)

################################
# Usar todas as colunas do df_IHRU como indicadores
indicadores_IHRU = list(df_IHRU.columns)

# Listar exclusivamente os indicadores disponíveis no df_IHRU
indicadores_IHRU = [col for col in df_IHRU.columns if col not in ['GEOID','geo_point_2d', 'year', 'dis_code', 'dis_name', 
                                                                  'con_code', 'con_name', 'con_name_upper', 
                                                                  'con_name_lower', 'con_area_code', 'con_type', 'geometry']]
# Criar menu de seleção para os indicadores
indicador_map_IHRU = st.sidebar.selectbox("Selecione o indicador de indignidade", indicadores_IHRU)

################################################################
# ----------------------------------------------------------------
# Ordenar valores para determinar Top 10 e Bottom 10
gdf_sorted = gdf.sort_values(by=indicador_selecionado, ascending=False)
top10 = gdf_sorted[["con_name_upper", indicador_selecionado]].head(10)
bottom10 = gdf_sorted[["con_name_upper", indicador_selecionado]].tail(10)

# Criar os gráficos interativos
max_scale = gdf[indicador_selecionado].max()  # Escala máxima para ambos os gráficos

fig_top = px.bar(
    top10,
    x=indicador_selecionado,
    y="con_name_upper",
    orientation="h",
    title="Top 10 Municípios",
    range_x=[0, max_scale],
    labels={"con_name_upper": "Município", indicador_selecionado: "Valor"}
)
fig_top.update_layout(yaxis=dict(autorange="reversed"))
fig_top.update_traces(marker_color="darkblue")

fig_bottom = px.bar(
    bottom10,
    x=indicador_selecionado,
    y="con_name_upper",
    orientation="h",
    title="Bottom 10 Municípios",
    range_x=[0, max_scale],
    labels={"con_name_upper": "Município", indicador_selecionado: "Valor"}
)
fig_bottom.update_traces(marker_color="grey")

#----------------------------------------------------------------
# Mapa Interativo
map_center = [39.6369, -8.0427]

# Criar o mapa base vazio com Folium
m = folium.Map(
    location=map_center,
    zoom_start=7,
    min_zoom=7,
    max_zoom=10,
    tiles=None  # Remove o mapa base padrão
)

# Adicionar o TileLayer opaco
folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr="&copy; <a href='https://www.carto.com/'>CARTO</a>",
    name="CartoDB Positron",
    opacity=0.01  # Define a opacidade como 100% (totalmente opaco)
).add_to(m)


# Criar o colormap para o indicador selecionado
colormap = linear.YlGnBu_09.scale(
    gdf[indicador_selecionado].min(),
    gdf[indicador_selecionado].max()
)

# Adicionar os polígonos ao mapa
def style_function(feature):
    value = feature['properties'].get(indicador_selecionado, None)
    return {
        'fillColor': colormap(value) if value is not None else 'transparent',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 1
    }

folium.GeoJson(
    gdf,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["con_name_upper", indicador_selecionado],
        aliases=["Município: ", f"{indicador_selecionado}: "],
        localize=True
    )
).add_to(m)

# Ajustar o estilo do mapa na página
map_width = "100%"    # Define a largura como 30% da tela
map_height = "660vh" # Define a altura como 680vh
m.get_root().width = map_width
m.get_root().height = map_height

# Desabilitar interações de zoom
m.options['scrollWheelZoom'] = False  # Desativa zoom por rolagem
m.options['doubleClickZoom'] = False  # Desativa zoom por duplo clique
colormap.caption = f"{indicador_selecionado}"
colormap.add_to(m)

#----------------------------------------------------------------
# Definir tamanhos fixos para os gráficos
largura_grafico = 1000  # Ajuste a largura desejada em pixels
altura_grafico = 650   # Ajuste a altura desejada em pixels

col1, col2 = st.columns([3, 5])

# Exibir o mapa no layout à esquerda
with col1:
    # st.title("Mapa de Indicadores de Habitação")
    st.components.v1.html(m._repr_html_(), height=900)

# Exibir gráficos ao lado direito
with col2:
    # Ajustar o tamanho do gráfico Top 10
    fig_top.update_layout(width=largura_grafico, height=altura_grafico)

    # Calcular estatísticas do indicador selecionado
    mean_value = gdf[indicador_selecionado].mean()
    std_dev = gdf[indicador_selecionado].std()
    median_value = gdf[indicador_selecionado].median()

    # Definir limites do intervalo
    lower_bound = mean_value - std_dev
    upper_bound = mean_value + std_dev

    # Selecionar os Top 10 e Bottom 10 municípios
    top_10 = gdf.nlargest(10, indicador_selecionado)
    bottom_10 = gdf.nsmallest(10, indicador_selecionado)

    # Configurar o gráfico de distribuição com Plotly
    fig = px.histogram(
        gdf,
        x=indicador_selecionado,
        nbins=60,
        title=f"Distribuição do Indicador: {indicador_selecionado}",
        template="plotly_white",
        color_discrete_sequence=["#9395ad"],  # Ajustar cor das barras
        opacity=0.8,  # Tornar as barras semitransparentes
    )

    # Adicionar linhas de média, limites e mediana
    fig.add_vline(
        x=mean_value,
        line_dash="dash",
        line_color="red",
        line_width=1,
        annotation_text=f"Média: {mean_value:.2f}",
        annotation_position="top right",
    )
    fig.add_vline(
        x=median_value,
        line_color="blue",
        line_width=1,
        annotation_text=f"Mediana: {median_value:.2f}",
        annotation_position="top left",
    )
    fig.add_vrect(
        x0=lower_bound,
        x1=upper_bound,
        fillcolor="grey",
        opacity=0.1,
        line_width=0,
        annotation_text="Média ± Desvio Padrão",
        annotation_position="bottom left",
    )

    # Adicionar destaque para cada município do Top 10
    for _, row in top_10.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row[indicador_selecionado]],
                y=[0],  # Alinhar marcadores na base do gráfico
                mode="markers",
                marker=dict(color="gold", size=12, symbol="circle-dot"),
                name=f"Top 10: {row['CONCELHO_DSG']}",
                text=f"{row['CONCELHO_DSG']}",
                hovertemplate="Município: %{text}<br>Valor: %{x:.2f}",
            )
        )

    # Adicionar destaque para cada município do Bottom 10
    for _, row in bottom_10.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row[indicador_selecionado]],
                y=[0],
                mode="markers",
                marker=dict(color="purple", size=12, symbol="square-dot"),
                name=f"Bottom 10: {row['CONCELHO_DSG']}",
                text=f"{row['CONCELHO_DSG']}",
                hovertemplate="Município: %{text}<br>Valor: %{x:.2f}",
            )
        )

    # Atualizar layout do gráfico de distribuição
    fig.update_layout(
        width=largura_grafico,  # Ajuste da largura
        height=altura_grafico,  # Ajuste da altura
        xaxis_title=f"Valores do Indicador: {indicador_selecionado}",
        yaxis_title="Frequência",
        legend_title="Municípios Destacados",
        title=dict(x=0.5),
        margin=dict(l=40, r=40, t=50, b=40),
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

################################

# Adicionar as tabelas de 2011 e 2021 no fundo da página
st.markdown("<h2 style='font-size: 18px; color: #46494d;'>Dados Detalhados</h2>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["2011", "2021"])

# Colunas a serem excluídas
colunas_excluidas = [
    'geo_point_2d', 'year', 'dis_code', 'dis_name', 'con_code', 'con_name',
    'con_name_upper', 'con_name_lower', 'con_area_code', 'con_type', 'geometry'
]

with tab1:
    st.dataframe(gdf2011.drop(columns=colunas_excluidas, errors="ignore"))  # Tabela para 2011

with tab2:
    st.dataframe(gdf2021.drop(columns=colunas_excluidas, errors="ignore"))  # Tabela para 2021