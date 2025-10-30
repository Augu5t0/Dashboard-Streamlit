# 🛍️ Dashboard de Vendas – Streamlit

![Demonstração do Dashboard](Dashboard.gif)

# 📊 Sobre o Projeto

Este projeto é um Dashboard Interativo de Vendas desenvolvido com Streamlit e Plotly, que consome dados da API pública LabDados
.

O objetivo é oferecer uma análise visual e dinâmica das vendas, permitindo explorar receitas, quantidades vendidas e desempenho de vendedores em diferentes regiões do Brasil.

# 🚀 Funcionalidades

✅ Filtros interativos na sidebar:

Região

Período (ano específico ou todo o histórico)

Categoria do produto

Vendedores

Tipo de pagamento

Faixa de preço, frete, parcelas e avaliação

✅ Visualizações dinâmicas:

Receita por estado (mapa geográfico)

Receita mensal por ano (gráfico de linha)

Top estados e categorias por receita e quantidade

Ranking dos melhores vendedores

✅ Página de dados brutos:

Tabela interativa com todos os registros filtráveis

Opção para baixar os dados em CSV com um clique

Exibição do número de linhas e colunas filtradas

✅ Multipáginas com Streamlit (Dashboard e Dados)

# 🧠 Tecnologias Utilizadas

Python 3.11+

Streamlit

Plotly Express

Pandas

Requests

# ⚙️ Como Executar o Projeto

##Clone o repositório

git clone https://github.com/Augu5t0/Dashboard-Streamlit.git
cd dashboard-vendas-streamlit

##Crie e ative um ambiente virtual

python -m venv venv
venv\Scripts\activate  # (Windows)

##ou

source venv/bin/activate  # (Linux/Mac)

##Instale as dependências

pip install -r requirements.txt

##Execute o Streamlit

streamlit run Dashboard.py

