# Libraries
# from haversine import haversine
import plotly.express as px
# import ploty.graph_objects as go

# # Bibliotecas necessarios
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static


st.set_page_config(page_title='Visão Empresa', page_icon='👔', layout='wide')
# ---------------------------------
# Funções
# ---------------------------------
def country_map(df1):
    df_aux = df1.loc[:, ['City', 'Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    map = folium.Map()
    for index,location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                location_info['Delivery_location_longitude']]).add_to(map)
    folium_static(map,width=1024, height=600)
    return None

def order_share_by_week (df1):
    # Quantidade de pedidos por entregador por Semana
    # Quantas entregas na semana / Quantos entregadores únicos por semana
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig

def order_by_week (df1):
    # Quantidade de pedidos por Semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='ID' )
    return fig

def traffic_order_city (df1):
    df_aux = (df1.loc[:, ['ID','City','Road_traffic_density']]
                 .groupby(['City','Road_traffic_density'])
                 .count()
                 .reset_index())
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    
    return fig

def order_metric (df1):
    #Seleção de linhas
    df_aux = df1.loc[:,['ID','Order_Date']].groupby('Order_Date').count().reset_index()
    # Desenhar o grafico
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df1):       
    df_aux = (df1.loc[:, ['ID','Road_traffic_density']]
                 .groupby('Road_traffic_density')
                 .count()
                 .reset_index())
    
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN']
    
    df_aux['entregas_perc'] = (df_aux['ID'] / df_aux['ID'].sum())
    
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
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
    
    # 7 - Limpando a time taken min
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# ----------------------------------- Inicio da estrutura logica do codigo ----------------------------

# -----------------------------------
# Import Dataset
# -----------------------------------
df = pd.read_csv('Dataset/train.csv')

#df1 = df.copy()

# -----------------------------------
# Limpando os dados
# -----------------------------------
df1 = clean_code (df)


# ============================================
# Barra lateral no streamlit
# ============================================
st.header('Marketplace - Visão empresa')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric
        fig = order_metric (df1)
        st.markdown('## Pedidos por dia')
        st.plotly_chart (fig,use_container_width=True)
   

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share (df1)
            st.markdown('### Pedidos por tráfego')
            st.plotly_chart(fig,use_container_width=True)
            

        with col2:
            fig = traffic_order_city(df1)
            st.markdown('### Pedidos por cidade e trafego')
            st.plotly_chart(fig,use_container_width=True)
            
            

with tab2:
    with st.container():
        st.markdown('### Pedidos por semana')
        fig = order_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
       
            

    with st.container():
        st.markdown('### Média de pedidos por entregador por semana')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
        
            


with tab3:
    st.markdown('# Mapa das entregas')
    country_map(df1)
    

    
        















