import streamlit as stl
import pandas as pd
import plotly.express as px

def aba_publico(partidas, estadios):

    coordenadas = {
        "Philadelphia": (39.9526, -75.1652),
        "New Jersey": (40.0583, -74.4057),
        "Atlanta": (33.7490, -84.3880),
        "Los Angeles": (34.0522, -118.2437),
        "Miami": (25.7617, -80.1918),
        "Orlando": (28.4159, -81.2988),    
        "Seattle": (47.6062, -122.3321),
        "Washington D.C": (38.9041, -77.0171),
        "Charlotte": (35.2062, -80.8326),
        "Nashville": (36.158204, -86.777239),
        "Cincinatti": (39.1399, -84.5064)
    }

    estadios['cidade'] = estadios['cidade'].replace({
        "Filadelfia": "Philadelphia",
        "Nova Iorque": "New Jersey"
    })

    estadios_por_cidade = estadios['cidade'].value_counts().reset_index()
    estadios_por_cidade.columns = ['cidade', 'num_estadios']

    estadios_mapa = estadios.drop_duplicates(subset=["cidade"]).merge(
        estadios_por_cidade, on='cidade', how='left'
    )
    estadios_mapa['latitude'] = estadios_mapa['cidade'].map(lambda x: coordenadas.get(x, (None, None))[0])
    estadios_mapa['longitude'] = estadios_mapa['cidade'].map(lambda x: coordenadas.get(x, (None, None))[1])

    partidas_por_cidade = partidas.merge(estadios[['id_estadio', 'cidade']], on='id_estadio')
    partidas_por_cidade = partidas_por_cidade['cidade'].value_counts().reset_index()
    partidas_por_cidade.columns = ['cidade', 'qtd_partidas']

    estadios_mapa = estadios_mapa.merge(partidas_por_cidade, on='cidade', how='left')

    if 'publico' not in partidas.columns:
        stl.error("A coluna 'publico' não está presente no DataFrame de partidas.")
        return

    media_publico = partidas['publico'].dropna().mean()
    total_estadios = estadios['nome'].nunique()

    col1, col2 = stl.columns(2)
    with col1:
        stl.markdown("""
        <div class="card">
        <h2>Média de Público</h2>
        <p style="font-size: 36px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)
        stl.metric("", f"{int(media_publico):,} mil".replace(",", ".").replace(".000 mil", " mil"))
    with col2:
        stl.markdown("""
        <div class="card">
        <h2>Total de Estádios</h2>
        <p style="font-size: 36px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)
        stl.metric("", f"{int(total_estadios):,} Estádios")

    fig_mapa = px.scatter_geo(
        estadios_mapa,
        lat="latitude",
        lon="longitude",
        hover_name="nome",
        text="cidade",
        size="qtd_partidas",
        title="Localização dos Estádios",
    )
    fig_mapa.update_geos(showcountries=True, showland=False, fitbounds="locations")
    fig_mapa.update_layout(height=500)
    stl.plotly_chart(fig_mapa, use_container_width=True)

    partidas_estadios = partidas.merge(estadios, on='id_estadio', how='left')

    stl.subheader("Média de Público por Estádio")

    media_por_estadio = partidas_estadios.groupby("nome")["publico"].mean().reset_index()
    media_por_estadio = media_por_estadio.sort_values("publico", ascending=False)
    media_por_estadio["nome"] = pd.Categorical(media_por_estadio["nome"], categories=media_por_estadio["nome"], ordered=True)

    fig_media = px.bar(
    media_por_estadio,
    x="publico",
    y="nome",
    orientation="h",
    title="Média de Público por Estádio",
    labels={"publico": "Média de Público", "nome": "Estádio"},
    text_auto=".0f",
    height=500
    )
    fig_media.update_layout(yaxis={'categoryorder': 'total ascending'})
    stl.plotly_chart(fig_media, use_container_width=True)

    stl.subheader("Número de Partidas por Estádio")

    partidas_count = partidas_estadios['nome'].value_counts().reset_index()
    partidas_count.columns = ['Estádio', 'Número de Partidas']

    fig_partidas = px.bar(
        partidas_count,
        x='Estádio',
        y='Número de Partidas',
        title="Quantidade de Partidas por Estádio",
        height=400
    )
    stl.plotly_chart(fig_partidas, use_container_width=True)
