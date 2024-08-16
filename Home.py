import streamlit as st
from PIL import Image

st.set_page_config(page_title = "Home",
                   page_icon = "")

#image_path = 'C:/Users/User/OneDrive/Documentos/repos/ftc_python_para_analise_de_dados/'
image= Image.open('target.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in town')
st.sidebar.markdown("""---""")

st.write(' # Curry Company dashboard')
st.markdown(
    """
    Dashboard planejado e construido para acompanhar as metricas de crescimento da empresa, analisando todos os setores
    envolvidos.
    ### Como utilizar esse Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais
        - Visão Tática: Indicadores de crescimento semanais
        - Visão Geográfica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores temporais de entrega dos pedidos.
     ### Ask for Help
     - https://www.linkedin.com/in/dagoberto-dinon-feiber-junior-b181361a6/
         -dagobertofeiber@gmail.com
""")