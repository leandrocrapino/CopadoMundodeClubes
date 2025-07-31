import streamlit as stl
import pandas as pd
import plotly.express as px

def aba_arbitragem(arbitragem, arbitros, partidas):

    arbitros.columns = arbitros.columns.str.strip().str.lower()
    arbitragem.columns = arbitragem.columns.str.strip().str.lower()
    partidas.columns = partidas.columns.str.strip().str.lower()

    arbitros['pais'] = arbitros['pais'].replace({   
    "Alemanha": "Germany",
    "Argelia": "Algeria",
    "Belgica": "Belgium",
    "Brasil": "Brazil",
    "Catar": "Qatar",
    "Croacia": "Croatia",
    "Egito": "Egypt",
    "Emirados Arabes Unidos": "United Arab Emirates",
    "Eslovaquia": "Slovakia",
    "Eslovenia": "Slovenia",
    "Espanha": "Spain",
    "Franca": "France",
    "Holanda": "Netherlands",
    "Inglaterra": "England",
    "Italia": "Italy",
    "Libia": "Libya",
    "Marrocos": "Morocco",
    "Noruega": "Norway",
    "Nova Zelandia": "New Zealand",
    "Paraguai": "Paraguay",
    "Polonia": "Poland",
    "Quenia": "Kenya",
    "Romenia": "Romania",
    "Suecia": "Sweden",
    "Uruguai": "Uruguay",
    "Uzbequistao": "Uzbekistan"
    })
    total_arbitros = arbitros['id_arbitro'].nunique()
    stl.metric("Número Total de Árbitros", total_arbitros)

    arbitragem_completa = arbitragem.merge(arbitros, on='id_arbitro')
    arbitragem_completa = arbitragem_completa.merge(partidas[['id_partida', 'fase']], on='id_partida')

    partidas_por_arbitro = arbitragem_completa['nome'].value_counts().reset_index()
    partidas_por_arbitro.columns = ['nome', 'partidas']
    
    fig_bar = px.bar(
        partidas_por_arbitro.head(10),
        x='partidas',
        y='nome',
        orientation='h',
        title='Quantidade de Partidas de Árbitros por Nome'
    )
    fig_bar.update_layout(title="Quantidade de Partidas de Árbitros por Nome",
        yaxis={'categoryorder': 'total ascending'},            
        xaxis_title="Partidas",
        yaxis_title="Nome",
        plot_bgcolor="white",
        height=600
    )

    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})

    stl.plotly_chart(fig_bar, use_container_width=True)

    arbitros_por_funcao = (
        arbitros.groupby('funcao')['id_arbitro']
        .nunique()
        .reset_index()
        .rename(columns={'id_arbitro': 'quantidade'})
    )
    
    fig_funcao = px.pie(
        arbitros_por_funcao,
        names='funcao',
        values='quantidade',
        title='Total de Árbitros por Função',
        hole=0.4
    )
    stl.plotly_chart(fig_funcao, use_container_width=True)

    ordem_fases = [
        "Fase de Grupos",
        "Oitavas de Final",
        "Quartas de Final",
        "SemiFinal",
        "Final"
    ]
    arbitragem_completa['fase'] = pd.Categorical(
        arbitragem_completa['fase'],
        categories=ordem_fases,
        ordered=True
    )

    matriz_fase = (
        arbitragem_completa.pivot_table(
            index='nome',
            columns='fase',
            values='id_partida',
            aggfunc='count',
            fill_value=0
        )
        .reset_index()
    )
    matriz_fase = matriz_fase[['nome'] + ordem_fases]
    stl.dataframe(matriz_fase)

    partidas_por_pais = arbitragem_completa.groupby('pais')['id_partida'].count().reset_index()
    fig_mapa = px.scatter_geo(
        partidas_por_pais,
        locations='pais',
        locationmode='country names',
        hover_name='pais',
        projection='natural earth',
        title='Quantidade de Partidas Apitadas por País'
    )
    stl.plotly_chart(fig_mapa, use_container_width=True)