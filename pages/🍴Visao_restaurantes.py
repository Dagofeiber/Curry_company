# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# # Bibliotecas necessarios
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurante', page_icon='🍴', layout='wide')

# ---------------------------------
# Funções
# ---------------------------------

def avg_std_time_on_traffic(df1):
                
    cols = ['City','Time_taken(min)','Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    
    fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], values='avg_time',
                      color='std_time',color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig
    
def avg_std_time_graph(df1):
    cols = ['City','Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                         x=df_aux['City'],
                         y=df_aux['avg_time'],
                         error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode = 'group')
    return fig

def avg_std_time_delivery(df1, festival, op):
    """ Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
            Parametros:
                Input:
                    - df: dataframe com os dados necessarios para o calculo
                    - op: tipo de operação que precisa ser calculado
                        ' avg_time': Calcula o tempo médio
                        ' std_time': Calcula o desvio padrão do tempo
                Output:
                    - df: Dataframe com 2 colunas e 1 linha.
        
    """
        
    cols = ['Festival','Time_taken(min)']
    df_aux = (df1.loc[:, cols]
                 .groupby(['Festival'])
                 .agg({'Time_taken(min)': ['mean','std']}))
    df_aux.columns = ['avg_time','std_time']
    df_aux['avg_time'] = df_aux['avg_time'].astype(float)
    df_aux = df_aux.reset_index() 
    df_aux = df_aux.loc[df_aux['Festival'] == festival, op]
    return df_aux

def distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 
                'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x: 
                              haversine ( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                              (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = round( df1['distance'].mean(), 2)
        return avg_distance
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine ( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
        avg_distance = df1.loc[:,['City','distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data= [go.Pie(labels=avg_distance['City'], values = avg_distance['distance'], pull = [0, 0.1, 0])])
        return fig
    
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
    df1.loc[:,'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # 7 - Limpando a time taken min
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# ------------------------------------
# Import Dataset
# ------------------------------------
df = pd.read_csv('Dataset/train.csv')
#df1 = df.copy()

#cleaning code
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
        col1, col2, col3 = st.columns([3,4,4])
        with col1:
            delivery_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique,)
            
        with col1:
            avg_distance = round(distance(df1, fig=False),2)
            col1.metric('Distância média das entregas', avg_distance)
            
            
        with col2:
            df_aux = round(avg_std_time_delivery(df1, 'Yes', 'avg_time'),2)
            col2.metric('Tempo médio de entrega com festival', df_aux)

        with col2:
            df_aux = round(avg_std_time_delivery(df1, 'Yes', 'std_time'),2)
            col2.metric('STD médio de entrega com festival', df_aux)
            
            
            
        with col3:
            df_aux = round(avg_std_time_delivery(df1, 'No', 'avg_time'),2)
            col3.metric('Tempo médio de entrega sem festival', df_aux)
            
            
        with col3:
            df_aux = round(avg_std_time_delivery(df1, 'No', 'std_time'),2)
            col3.metric('STD médio de entrega sem festival', df_aux)
            

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2,gap='medium')
        with col1:
            st.markdown('### Tempo médio de entrega por cidade')
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)

        with col2:
            st.markdown('### Tempo médio de entrega por tipo de pedido')
            cols = ['City','Time_taken(min)','Type_of_order']
            df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time','std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
            

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""---""")
            st.markdown('### Média da distancia de entrega por tipo de cidade')
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)
 
        
        with col2:
            st.markdown("""---""")
            st.markdown('### Distribuição do tempo de entrega')
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)

    
    with st.container():
        st.markdown("""---""")
        st.markdown('### Distribuição dos tempos de entrega por tipo de pedido')
        cols = ['City','Time_taken(min)','Type_of_order']
        df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux,width=1000)
        
    