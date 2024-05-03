import os
import streamlit as st

DATA_DIR = "data"
ALL_FILES = []
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        ALL_FILES.append(os.path.join(root, file))


def intro():
    import streamlit as st

    st.write("# Ambiente de Dados da Codaqui! 👋")
    st.write(
        """
Este é um ambiente de dados para a Codaqui. Aqui você pode visualizar e analisar os dados da ONG! 😃

![Imagem](https://github.com/codaqui/institucional/raw/main/images/header.png)

A Codaqui.dev tem o prazer de apresentar nosso novo Ambiente de Dados.

Com este ambiente, estamos capacitando nossos alunos a estudar e tomar decisões baseadas em dados,
impulsionando a inovação e promovendo a excelência em todas as nossas operações.
Estamos ansiosos para ver as incríveis soluções e descobertas que surgirão deste ambiente.

Junte-se a nós nesta emocionante jornada de descoberta de dados na [Codaqui.dev](https://www.codaqui.dev)!

"""
    )


def read_pages_info_files():
    import streamlit as st
    import pandas as pd

    # Filter only pages_info files
    pages_info_files = [file for file in ALL_FILES if "pages_info" in file]

    # Read all pages_info files
    dataframe_list = []
    for file in pages_info_files:
        dataframe_list.append(pd.read_json(file))

    # Concatenate all DataFrames
    dataframe_with_all = pd.concat(dataframe_list)

    # Concat 2 columns to create a new one
    dataframe_with_all["year-month"] = (
        dataframe_with_all["year"].astype(str)
        + "-"
        + dataframe_with_all["month"].astype(str)
    )

    # Páginas mais acessadas
    st.write("## Páginas mais acessadas")
    st.write("Selecione o intervalo de tempo:")
    min_year = dataframe_with_all["year"].min()
    max_year = dataframe_with_all["year"].max()
    min_month = dataframe_with_all["month"].min()
    max_month = dataframe_with_all["month"].max()
    year = st.slider("Ano", min_value=min_year - 1, max_value=max_year)
    month = st.slider("Mês", min_value=min_month, max_value=max_month)
    filtered_data = dataframe_with_all[
        (dataframe_with_all["year"] == year) & (dataframe_with_all["month"] == month)
    ]
    filtered_data = filtered_data.sort_values(by="activeUsers", ascending=False)
    top_10 = filtered_data.head(10)
    st.bar_chart(top_10.set_index("pagePath")["activeUsers"])

    return "Ok"


page_names_to_funcs = {"—": intro, "Páginas": read_pages_info_files}

page_name = st.sidebar.selectbox("Selecione uma página:", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
