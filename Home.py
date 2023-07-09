import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    #page_icon=""

)


#image_path = 'Delivery.png'
image = Image.open( 'Delivery.png' )
st.sidebar.image( image, width=300)

st.sidebar.markdown ('# Curry Company')
st.sidebar.markdown ('## A entrega mais rápida da cidade')
st.sidebar.markdown ("""---""")

st.write ( '# Painel de Crescimento - Curry Company' )

st.markdown( 
    """
    Growth Dashboard foi construído para acompanhar a métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização.
    - Visão entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ajuda
    - jbridi@gmail.com
    """)