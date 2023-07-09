# bibliotecas

from haversine import haversine
import plotly.express as px
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão_Entregadores', page_icon='', layout='wide' )

#------------------------------------------
# Funções
#------------------------------------------
def top_delivers ( df1, top_asc ):
    df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
               .groupby(['City', 'Delivery_person_ID'])
               .mean()
               .sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
               .reset_index() )

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian' , :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban' , :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi_Urban' , :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
                    
    return df3

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

st.header('Marketplace - Visão Entregadores')

#image_path = 'Delivery.png'
image = Image.open( 'Delivery.png' )
st.sidebar.image( image, width=300)

st.sidebar.markdown ('# Curry Company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.sidebar.markdown ('## Selecione uma data limite')

date_slider  = st.sidebar.slider(
    'Até qual valor?', 
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY')


st.sidebar.markdown("""----""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
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

# criar visões
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])


with tab1:
# criar container
    with st.container():
        st.title( 'Métricas Gerais' )
        
# criar colunas
        col1, col2, col3, col4 = st.columns( 4, gap= 'large' ) 
        with col1:
            # Maior idade dos entregadores
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric( 'Maior Idade', maior_idade )
          
        with col2:
            # Menor idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric( 'Menor Idade', menor_idade )
            
        with col3:
            # melhor condição de veículo           
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric( 'Melhor Condição de Veículo', melhor_condicao )
            
        with col4:
            # pior condição de veículo
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric( 'Pior condiçâo de veículo', pior_condicao )

    with st.container():
        st.markdown("""___""")
        st.title( 'Avaliações' )
        
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown ( '##### Avaliações Média por Entregador' )
            df_avg_ratings_per_deliver = ( df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                              .groupby( 'Delivery_person_ID' )
                                              .mean()
                                              .reset_index() )
            st.dataframe( df_avg_ratings_per_deliver )
            

            
        with col2:
            st.markdown( '##### Avaliação Média por Trânsito' )
            df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                                .groupby( 'Road_traffic_density' )
                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # mudança nome colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            # reset index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe ( df_avg_std_rating_by_traffic)
            st.markdown( '##### Avaliação Média por Clima' )
            

            df_avg_std_rating_by_Weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                                .groupby( 'Weatherconditions' )
                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            # mudança nome colunas
            df_avg_std_rating_by_Weather.columns = ['delivery_mean', 'delivery_std']

            # reset index
            df_avg_std_rating_by_Weather = df_avg_std_rating_by_Weather.reset_index()
            st.dataframe( df_avg_std_rating_by_Weather )
            
            
            
            
    with st.container():
        st.markdown ("""___""")
        st.title( 'Velocidade de Entrega' )
        
        col1, col2 = st.columns( 2 )
        
        with col1:
            st.markdown( '##### Top Entregadores mais Rápidos' )
            df3 = top_delivers ( df1, top_asc=True )
            st.dataframe ( df3 )

            
        with col2:
            st.markdown( '##### Top Entregdores mais Lentos' )
            df3 = top_delivers ( df1, top_asc=False )
            st.dataframe ( df3 )
                

                
                
                
            
            
        
        
        
            
    

