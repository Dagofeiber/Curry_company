# Libraries
# from haversine import haversine
import plotly.express as px
#import ploty.graph_objects as go

# # Bibliotecas necessarios
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Entregadores', page_icon='🛵', layout='wide')

# ---------------------------------
# Funções
# ---------------------------------

def top_deliveries (df1,top_asc):
    df_aux = (df1.loc[:, ['Delivery_person_ID','City','Time_taken(min)']]
                 .groupby(['City','Delivery_person_ID'])
                 .mean()
                 .sort_values(['City','Time_taken(min)'], ascending = top_asc)
                 .reset_index())
    df_aux1 = df_aux.loc[df_aux['City'] == 'Metropolitian',:].head(10)
    df_aux2 = df_aux.loc[df_aux['City'] == 'Urban',:].head(10)
    df_aux3 = df_aux.loc[df_aux['City'] == 'Semi-Urban',:].head(10)
    df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
    return df2

def clean_code (df1):
    """ Esta função tem a responsabilidade de limpar o dataframe

    Tipos de limpeza:
    1. Remoção dos dados Nan
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variaveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variavel numerica)

    Input: Dataframe
    output: Dataframe
    
    """
    # 1 - Convertendo a coluna Age de texto para numero
    linhas_e = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_e, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype('int32')
    
    # Removendo NaN da coluna densidade
    linhas_es = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_es,:].copy()
    
    # Removendo NaN da coluna city
    linhas_es = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_es,:].copy()
    
    # Removendo NaN da coluna festival
    linhas_es = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_es,:].copy()
    
    # 2 - Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    
    # 3 - Conversao de texto para data
    linhas_v = df1['Order_Date'] != 'NaN '
    df1 = df1.loc[linhas_v, :]
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )
    
    # 4 - Convertendo 'multiple_deliveries' de texto para numero inteiro
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype('int32')
    
    # 5 - Remover spaco da string
    # df1 = df1.reset_index(drop = True)
    # for i in range( len( df ) ):
    # df1.loc[i, 'ID'] = df.loc[i, 'ID'].strip()
    # df1.loc[i, 'Delivery_person_ID'] = df1.loc[i, 'Delivery_person_ID'].strip()
    
    # 6 - Removendo espaços da string sem o for
    df1.loc[:,'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:,'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:,'City'] = df1.loc[:, 'City'].str.strip()
    
    # 7 - Limpando a time taken min
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1
# Import Dataset
df = pd.read_csv('Dataset/train.csv')

# df1 = df.copy()

# cleaning dataset
df1 = clean_code(df)

# ============================================
# Barra lateral no streamlit
# ============================================
st.header('Marketplace - Visão entregadores')

#image_path = 'target.jpg'
image = Image.open ('target.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest delivery in town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022,4,13),
    min_value=datetime(2022,2,11),
    max_value=datetime(2022,4,6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'])

st.sidebar.markdown("""---""")
#st.sidebar.markdown('### Powered by Dagoberto')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]



# ============================================
# Layout no streamlit
# ============================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    with st.container():
        st.title('Métricas gerais')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            # a maior idade dos entregadores
            maior_idade = (df1.loc[:, 'Delivery_person_Age'].max())
            col1.metric('Maior idade', maior_idade)
            
        with col2:
            # a menor idade dos entregadores
            menor_idade = (df1.loc[:, 'Delivery_person_Age'].min())
            col2.metric('Menor idade', menor_idade)
            
        with col3:
            # a melhor condição de veiculo
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição de veiculo', melhor_condicao)
            
        with col4:
            # a pior condição de veiculo
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição de veiculo', pior_condicao)

    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliações média por entregador')
            df_media_por_entregador = (df1.loc[:, ['Delivery_person_Ratings','Delivery_person_ID']]
                                       .groupby('Delivery_person_ID')
                                       .mean()
                                       .reset_index())
            st.dataframe(df_media_por_entregador)

        with col2:
            st.markdown('##### Avaliação média por transito')
            df_aux = (df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                         .groupby('Road_traffic_density')
                         .agg({'Delivery_person_Ratings':['mean','std']}))
            # Mudança de nome das colunas
            df_aux.columns = ['Delivery_mean', 'Delivery_std']
            #reset do index
            df_aux.reset_index()
            st.dataframe(df_aux)
            
            st.markdown('##### Avaliação média por clima')
            df_aux = (df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
                         .groupby('Weatherconditions')
                         .agg({'Delivery_person_Ratings':['mean','std']}))
            df_aux.columns = ['Delivery_mean', 'Delivery_std']
            df_aux.reset_index()
            st.dataframe(df_aux)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top entregadores mais rapidos')
            df2 = top_deliveries(df1,top_asc=True)
            st.dataframe(df2)

        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df2 = top_deliveries(df1,top_asc=False)
            st.dataframe(df2)
            
                
            
