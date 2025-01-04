import streamlit as st
from PIL import Image

# Configurar página
st.set_page_config(page_title="Portal HABITA",  layout="wide")
################################################################


################################################################
# Título e introdução
col1, col2, col3 = st.columns([1, 10, 1])  # Ajuste proporcional para centralizar
with col2:
    st.title("Portal HABITA - Indicadores de Habitação")
    st.divider()

################################################################
# Carregar e centralizar a imagem
image = Image.open("Picture1.jpg")
col1, col2, col3 = st.columns([5, 3, 5])  # Ajuste proporcional para centralizar
with col2:
    st.image(image, width=300, use_container_width=True)

################################################################
col1, col2, col3 = st.columns([1, 8, 1])  # Ajuste proporcional para centralizar
with col2:
    st.write("Explore os dados e análises interativas sobre padrões territoriais de habitação em 2011 a 2021, nos menus:")


################################################################
# Menus no topo (tabs)
tab1, tab2, tab3 = st.tabs(["Descrição", "Sobre o Projeto", "Indicadores"])

# Conteúdo das abas
with tab1:
    st.subheader("Descrição")
    st.write(
        """
        Este portal apresenta indicadores sobre a habitação em Portugal, consolidando informações essenciais para apoiar 
        a compreensão das dinâmicas habitacionais no país. Com foco em promover uma análise consistente e territorialmente 
        desagregada, o conteúdo disponibilizado visa contribuir para a formulação de estratégias eficazes que enfrentem 
        os desafios habitacionais e promovam a habitação digna e acessível para todos.
        
        **Principais Objetivos:**
        - Oferecer uma visão geral sobre o panorama habitacional em Portugal, destacando a diversidade e os desafios enfrentados nos diferentes territórios.
        - Consolidar dados e informações habitacionais, organizados de forma acessível e integradora, para subsidiar discussões e decisões informadas.
        - Promover reflexões e debates sobre políticas habitacionais, incentivando soluções inovadoras e sustentáveis para a melhoria das condições habitacionais no país.
        """
    )

with tab2:
    st.subheader("Sobre o Projeto")
    st.write(
        """
        Este portal foi desenvolvido com a coordenação científica da Universidade de Aveiro e o apoio da equipa técnica do 
        GETIN_UA – Grupo de Estudos em Território e Inovação.
        
        **Ficha Técnica:**
        - **Equipa Técnica:** GETIN_UA – Grupo de Estudos em Território e Inovação; Universidade de Aveiro.
        """
    )

with tab3:
    st.subheader("Indicadores")
    st.write(
        """
        Este portal integra dados relevantes sobre o setor habitacional em Portugal, oferecendo suporte para uma compreensão 
        clara dos principais desafios enfrentados por diferentes territórios. A organização das informações visa não apenas 
        documentar a realidade habitacional, mas também criar uma base sólida para a elaboração de estratégias que garantam 
        o acesso universal a uma habitação digna e adequada.
        """
    )

    # Lista de Indicadores
    indicadores = {
        "Indice_Volumetria_2011": "Índice de volumetria do edificado em 2011.",
        "Percentagem_Vagos_2011": "Percentagem de alojamentos vagos em 2011.",
        "Idade_Media_Edif_2011": "Idade média dos edifícios em 2011.",
        "Percentagem_Alojamento_Habitual_2011": "Percentagem de alojamentos de residência habitual em 2011.",
        "Dimensao_Alojamento_2011": "Dimensão média dos alojamentos (m²) em 2011.",
        "Alojamento_Por_Familia_2011": "Número de alojamentos por família em 2011.",
        "Percentagem_Arrendamento_2011": "Percentagem de alojamentos em regime de arrendamento em 2011.",
        "Numero_Divisoes_2011": "Número médio de divisões por alojamento em 2011.",
        "Indicador_Acessibilidade_Economica_2011": "Indicador de acessibilidade econômica ao mercado habitacional em 2011.",
        "Alojamento_Por_Familias_2021_2011": "Variação no número de alojamentos por família entre 2011 e 2021."
    }

    st.write("### Lista de Indicadores:")
    for key, value in indicadores.items():
        st.markdown(f"**{key}:** {value}")

    # Explicação adicional
    st.write(
        """
        Estes indicadores foram utilizados para analisar as dinâmicas habitacionais no país, incluindo aspectos como 
        idade média do edificado, distribuição dos alojamentos, arrendamento, e acessibilidade econômica. A interpretação 
        desses indicadores é essencial para compreender as características e os desafios do setor habitacional em diferentes territórios.
        """
    )
