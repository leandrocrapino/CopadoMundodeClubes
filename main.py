import streamlit as stl
import pandas as pd
import plotly.express as px
from Clubes import aba_clubes
from Resultados import aba_resultados
from Publico import aba_publico
from Arbitragem import aba_arbitragem
from PIL import Image

def carregar_estilo():
    with open("style.css") as f:
        stl.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
carregar_estilo()

df = pd.read_excel("data/CopadoMundodeClubes.xlsx")
df.head()

stl.set_page_config(page_title="Copa do Mundo de Clubes 2025", layout="wide")

col1, col2, col3 = stl.columns([1, 6, 1])
with col1:
    stl.image("logo_fifa.png", width=100)
with col2:
    stl.title("Análise de Dados Copa do Mundo de Clubes 2025")
with col3:
    stl.image("logo_copa.png", width=100)

def load_data():
    arbitros = pd.read_csv("data/CopadoMundodeClubes - Arbitros.csv")
    arbitragem = pd.read_csv("data/CopadoMundodeClubes - Arbitragem.csv")
    clubes = pd.read_csv("data/CopadoMundodeClubes - Clubes.csv")
    estadios = pd.read_csv("data/CopadoMundodeClubes - Estadios.csv")
    partidas = pd.read_csv("data/CopadoMundodeClubes - Partidas.csv")
    return arbitros, arbitragem, clubes, estadios, partidas

arbitros, arbitragem, clubes, estadios, partidas = load_data()

aba = stl.sidebar.radio("Abas:", [
    "Resultados",
    "Clubes",
    "Público",
    "Arbitragem"
])

if aba == "Resultados":
    stl.header("Resultados")
    stl.info("Gráficos com os resultados dos jogos.")
    (aba_resultados(partidas, clubes))

elif aba == "Clubes":
    stl.header("Clubes")
    stl.info("Análise por confederação, país e valor de elenco.")
    (aba_clubes(clubes))

elif aba == "Público":
    stl.header("Público")
    stl.info("Capacidade, cidades, média de público e ocupação por estádio.")
    (aba_publico(partidas, estadios))

elif aba == "Arbitragem":
    stl.header("Arbitragem")
    stl.info("Análise de árbitros, assistentes e VAR.")
    (aba_arbitragem(arbitragem, arbitros, partidas))