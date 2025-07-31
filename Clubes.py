import streamlit as stl
import pandas as pd
import plotly.express as px

def aba_clubes(clubes):
    clubes["valor_elenco(mi de euros)"] = (
    clubes["valor_elenco(mi de euros)"]
    .astype(str)                      
    .str.replace(".", "", regex=False)  
    .str.replace(",", ".", regex=False)  
    .astype(float)                   
)
    clubes['pais'] = clubes['pais'].replace({   
    "EUA": "United States",
    "Brasil": "Brazil",
    "Nova Zelandia": "New Zealand",  
    "Arabia Saudita": "Saudi Arabia",
    "Espanha": "Spain",
    "Italia": "Italy",
    "Alemanha": "Germany",
    "Africa do Sul": "South Africa",
    "Japao": "Japan",
    "Coreia do Sul": "South Korea",
    "Egito": "Egypt",
    "Franca": "France",
    "Inglaterra": "England",
    "Marrocos": "Morocco"

})
    clubes_por_pais = clubes["pais"].value_counts().reset_index()
    clubes_por_pais.columns = ["pais", "qtd_clubes"]

    clubes_mapa = clubes.drop_duplicates(subset=["pais"]).merge(clubes_por_pais, on="pais", how="left")

    fig_donut = px.pie(clubes, names="confederacao", title="Distribuição de Clubes por Confederação", hole=0.5)
    stl.plotly_chart(fig_donut, use_container_width=True)

    fig_mapa = px.scatter_geo(clubes_mapa,
                          locations="pais",
                          locationmode="country names",
                          hover_name="pais",
                          size="qtd_clubes",
                          title="País de Origem dos Clubes")
    stl.plotly_chart(fig_mapa, use_container_width=True)

    fig_bar = px.bar(clubes.sort_values("valor_elenco(mi de euros)", ascending=False),
                     x="sigla_clube",
                     y="valor_elenco(mi de euros)",
                     title="Valor de Elenco por Clube")
    stl.plotly_chart(fig_bar, use_container_width=True)