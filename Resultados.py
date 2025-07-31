import streamlit as stl
import pandas as pd
import plotly.express as px

stl.set_page_config(page_title="Resultados - Copa do Mundo de Clubes", layout="wide")

def aba_resultados(partidas, clubes):

    partidas = partidas.merge(clubes[['id_clube', 'nome_clube']], left_on='id_time_a', right_on='id_clube', how='left').rename(columns={'nome_clube': 'time a'})
    partidas = partidas.merge(clubes[['id_clube', 'nome_clube']], left_on='id_time_b', right_on='id_clube', how='left').rename(columns={'nome_clube': 'time b'})

    partidas['resultado'] = partidas.apply(
        lambda row: 'time a' if row['gols_time_a'] > row['gols_time_b']
        else 'time b' if row['gols_time_a'] < row['gols_time_b']
        else 'Empate',
        axis=1
    )
    partidas['gols_total'] = partidas['gols_time_a'] + partidas['gols_time_b']

    partidas['placar_original'] = partidas.apply(lambda row: f"{row['gols_time_a']} x {row['gols_time_b']}", axis=1)

    partidas['placar_ordenado'] = partidas.apply(
        lambda row: tuple(sorted([row['gols_time_a'], row['gols_time_b']])), axis=1
    )

    freq = partidas.groupby('placar_ordenado').size().reset_index(name='frequencia')

    mais_comuns = (
    partidas.groupby('placar_ordenado')['placar_original']
    .agg(lambda x: x.value_counts().idxmax())
    .reset_index()
    )

    placares = freq.merge(mais_comuns, on='placar_ordenado')
    placares = placares[['placar_original', 'frequencia']].rename(columns={'placar_original': 'placar'})

    placares = placares.sort_values(by='frequencia', ascending=False).head(10)    
    mais_comum = placares.head(1)

    total_gols = partidas['gols_total'].sum()
    total_partidas = len(partidas)
    total_empates = (partidas['resultado'] == 'Empate').sum()

    col1, col2, col3, col4 = stl.columns(4)
    with col1:
        stl.markdown("""
    <div class="card">
    <h2>Placar Mais Comum</h2>
    <p style="font-size: 36px; font-weight: bold;"></p>
    </div>
    """, unsafe_allow_html=True)
        stl.metric(label="", value=mais_comum['placar'].values[0])       

    with col2:
        stl.markdown("""
        <div class="card">
        <h2>Total de Gols</h2>
        <p style="font-size: 36px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)
        stl.metric(label="", value=total_gols)     

    with col3: 
        stl.markdown("""
        <div class="card">
        <h2>Total de Partidas</h2>
        <p style="font-size: 36px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)
        stl.metric(label="", value=total_partidas)     
    
    with col4:
        stl.markdown("""
        <div class="card">
        <h2>Quantidade de Empates</h2>
        <p style="font-size: 36px; font-weight: bold;"></p>
        </div>
        """, unsafe_allow_html=True)
        stl.metric(label="", value=total_empates) 

    stl.subheader("Placares Mais Frequentes")
    fig3 = px.bar(
        placares,
        x='placar',
        y='frequencia',
        text='frequencia',
        labels={'placar': 'Placar', 'frequencia': 'Frequência'}
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(xaxis_title="Placar", yaxis_title="Frequência")
    stl.plotly_chart(fig3, use_container_width=True)
    ordem_fases = [
        "Fase de Grupos", 
        "Oitavas de Final", 
        "Quartas de Final", 
        "SemiFinal", 
        "Final"
    ]
    partidas['fase'] = pd.Categorical(partidas['fase'], categories=ordem_fases, ordered=True)

    stl.subheader("Média de Gols por Fase")
    media_gols_fase = partidas.groupby('fase')['gols_total'].mean().reset_index()
    fig1 = px.bar(
        media_gols_fase,
        x='fase',
        y='gols_total',
        labels={'fase': 'Fase', 'gols_total': 'Média de Gols'}
    )
    fig1.update_layout(xaxis_title="Fase", yaxis_title="Média de Gols")
    stl.plotly_chart(fig1, use_container_width=True)