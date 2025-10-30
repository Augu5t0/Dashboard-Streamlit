import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS ')

url = 'https://labdados.com/produtos'
regioes = ['Brasil','Centro-Oeste','Nordeste','Norte','Sudeste','Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_ano = st.sidebar.checkbox('Dados de todo o período', value=True)
if todos_ano:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao':regiao.lower(), 'ano':ano}

reponse = requests.get(url, params=query_string)
dados = pd.DataFrame.from_dict(reponse.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

filtro_vendedores = st.sidebar.multiselect('Vendedores',dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]

## Tabelas

## Tabelas de Receita

receita_estado = dados.groupby('Local da compra')[['Preço']].sum()
receita_estado = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estado, left_on='Local da compra', right_index=True).sort_values(by='Preço', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq= 'ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)

## Tabelas de Quantidade de vendas

qtd_estado = dados.groupby('Local da compra')[['Preço']].count().rename(columns={'Preço': 'Quantidade'})
qtd_estado = (
    dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']]
    .merge(qtd_estado, left_on='Local da compra', right_index=True)
    .sort_values(by='Quantidade', ascending=False)
)

qtd_mensal = (
    dados.set_index('Data da Compra')
    .groupby(pd.Grouper(freq='ME'))['Preço']
    .count()
    .reset_index()
)
qtd_mensal['Ano'] = qtd_mensal['Data da Compra'].dt.year
qtd_mensal['Mes'] = qtd_mensal['Data da Compra'].dt.month_name()

qtd_categorias = dados.groupby('Categoria do Produto')[['Preço']].count().rename(columns={'Preço': 'Quantidade'}).sort_values(by='Quantidade', ascending=False)

## Tabelas vendedores

vendedores = (
    dados.groupby('Vendedor')['Preço']
    .agg(['sum', 'count'])
    .sort_values(by='sum', ascending=False)
    .reset_index()
)

#Gráficos

#Gráficos de receita
fig_mapa_receita = px.scatter_geo(receita_estado,
                                  lat='lat',
                                  lon='lon',
                                  scope='south america',
                                  size='Preço',
                                  template='seaborn',
                                  hover_name='Local da compra',
                                  hover_data={'lat': False, 'lon':False},
                                  title='Receita por Estado')

fig_receita_mensal = px.line(receita_mensal,
                             x='Mes',
                             y='Preço',
                             markers=True,
                             range_y = (0, receita_mensal.max()),
                             color='Ano',
                             line_dash='Ano',
                             title='Receita Mensal'
                             )

fig_receita_mensal.update_layout(yaxis_title='Receita')

fig_receita_estados = px.bar(receita_estado.head(5),
                             x='Local da compra',
                             y='Preço',
                             text_auto=True,
                             title='Top Estados (receita)')

fig_receita_estados.update_layout(yaxis_title='Receita')

fig_receita_categorias = px.bar(receita_categorias,
                                text_auto=True,
                                title='Receita por categorias')

fig_receita_categorias.update_layout(yaxis_title='Receita')

#Gráficos de quantidade de vendas

fig_mapa_quantidade = px.scatter_geo(qtd_estado,
                                  lat='lat',
                                  lon='lon',
                                  scope='south america',
                                  size='Quantidade',
                                  template='seaborn',
                                  hover_name='Local da compra',
                                  hover_data={'lat': False, 'lon':False},
                                  title='Quantidade de vendas por Estado')

fig_quantidade_mensal = px.line(qtd_mensal,
                             x='Mes',
                             y='Preço',
                             markers=True,
                             range_y = (0, qtd_mensal.max()),
                             color='Ano',
                             line_dash='Ano',
                             title='Quantidade de vendas mensal'
                             )

fig_quantidade_mensal.update_layout(yaxis_title='Quantidade')

fig_quantidade_estados = px.bar(qtd_estado.head(5),
                             x='Local da compra',
                             y='Quantidade',
                             text_auto=True,
                             title='Top Estados (Quantidade)')

fig_quantidade_estados.update_layout(yaxis_title='Quantidade')

fig_quantidade_categorias = px.bar(qtd_categorias,
                                text_auto=True,
                                title='Quantidade de vendas por categorias')

fig_quantidade_categorias.update_layout(yaxis_title='Quantidade')


# Visualização no Streamlit

aba1,aba2,aba3 = st.tabs(['Receita', 'Quantidade de Vendas', 'Vendedores'])

with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categorias, use_container_width=True)
with aba2:
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_quantidade, use_container_width=True)
        st.plotly_chart(fig_quantidade_estados, use_container_width=True)
    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_quantidade_mensal, use_container_width=True)
        st.plotly_chart(fig_quantidade_categorias, use_container_width=True)
with aba3:
    col1, col2 = st.columns(2)
    with col1:
        qtd_vendedores = st.number_input('Quantidade de Vendedores', 2, 10, 5)
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        
        fig_receita_vendedores = px.bar(
            vendedores.head(qtd_vendedores),
            x='sum',
            y='Vendedor',
            text_auto=True,
            title=f'Top {qtd_vendedores} vendedores (receita)'
        )
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)
    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        fig_vendas_vendedores = px.bar(
            vendedores.sort_values('count', ascending=False).head(qtd_vendedores),
            x='count',
            y='Vendedor',
            text_auto=True,
            title=f'Top {qtd_vendedores} vendedores (quantidade)'
        )
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)

