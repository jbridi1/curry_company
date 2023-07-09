# bibliotecas

from haversine import haversine
import plotly.express as px
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config( page_title='Visão_Empresa', page_icon='', layout='wide' )

#------------------------------------------
# Funções
#------------------------------------------
def country_maps ( df1 ):
    df_aux = ( df1.loc[:, [ 'City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .groupby(['City', 'Road_traffic_density'])
                  .median()
                  .reset_index() )

    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)


    folium_static(map, width=1024, height=600)
            
def order_share_week ( df1 ):
    df_aux1 = ( df1.loc[:, ['ID', 'week_of_year']]
                   .groupby( 'week_of_year')
                   .count()
                   .reset_index() )
    df_aux2 = ( df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                   .groupby( 'week_of_year')
                   .nunique()
                   .reset_index() )

    # juntar 2 tabelas (dataframe)
    df_aux = pd.merge( df_aux1, df_aux2, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
            
    return fig
        
def order_by_week( df1 ): 
    #criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U')
    df_aux = ( df1.loc[:, ['ID', 'week_of_year']]
                  .groupby('week_of_year')
                  .count()
                  .reset_index() )

    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig
        
def traffic_order_city( df1 ): 
    df_aux = ((df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .count()
                  .reset_index()))
                
    fig = px.scatter( df_aux, x='City', y='Road_traffic_density', size= 'ID', color='City')
                
    return fig
            
        
def traffic_order_share( df1 ):             
    df_aux = ((df1.loc[:, ['ID', 'Road_traffic_density']]
                  .groupby('Road_traffic_density')
                  .count()
                  .reset_index()))
    
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie( df_aux, values= 'entregas_perc', names='Road_traffic_density')
                
    return fig
                
def order_metric( df1 ):
    cols = ['ID', 'Order_Date']
    #seleção de linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

    #desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Order_Date', y='ID')
            
    return fig


def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
    
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo de coluna de dados
        3. Remoção dos espaços das variáveis de testo
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Imput: Dataframe
        Output: Dataframe
    """
    # 1. convertendo a coluna Age, de texto para numero
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )


    # 2. convertendo a coluna Ratings, de texto para numero decimal ( float )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype ( float )

    # 3. convertendo a coluna order_date, de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    # 4. convertendo multiple_deliveries, de texto para numero inteiro ( int )
    linhas_selecionadas = (df1['multiple_deliveries'] != 'Nan ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( float )

    ## 5. Removendo os espaços dentro de strings/texto/object
    #df1 = df1.reset_index( drop=true )
    #for i in range( len( df1 )):
    #  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

    # 6. Removendo os espaços dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()


    # 7. Limpando coluna de time taken

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# --------------------------------------------- Ínicio da Estrutura Lógica do Código ---------------------------------------------

# --------------------
# import dataset
# --------------------

df = pd.read_csv( 'dataset/train.csv' )

#---------------------
# Limpando os dados
# --------------------
df1 = clean_code( df )



# ====================================
# Barra Lateral
# ====================================
st.header('Marketplace - Visão Cliente')

#image_path = 'Delivery.png'
image = Image.open( 'Delivery.png' )
st.sidebar.image( image, width=300)

st.sidebar.markdown ('# Curry Company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.sidebar.markdown ('## Selecione uma data limite')

date_slider  = st.sidebar.slider(
    'Defina as Datas', 
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY')


st.sidebar.markdown("""----""")

traffic_options = st.sidebar.multiselect(
    'Escolha as condições de trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Jean Paulo Bridi')

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Trafico
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]



# ====================================
# layout no streamlit
# ====================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # order matric
        st.header('Entregas por Dia')
        fig = order_metric( df1 )
        st.plotly_chart(fig, use_container_width=True)
          
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1: 
            st.header('Tipo de transito por Entrega ')
            fig = traffic_order_share ( df1 )
            st.plotly_chart(fig, use_container_width=True)
                           
        with col2:  
            st.header('Tipo de transito por Entrega por Cidade')
            fig = traffic_order_city( df1 )
            st.plotly_chart(fig, use_container_width=True)
            
                
with tab2:
    with st.container():
        st.header('Pedidos por Semana')
        fig = order_by_week ( df1 )
        st.plotly_chart(fig, use_container_width=True)
           
    with st.container():
        st.header('Pedidos por Entregador por Semana')
        fig = order_share_week ( df1 )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header ('Localização no Mapa')
    country_maps ( df1 )

    
    
    

    

