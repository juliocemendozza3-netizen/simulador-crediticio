import streamlit as st
import pandas as pd
import joblib
import gspread
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
from google.oauth2.service_account import Credentials

from styles import aplicar_estilos


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Banco Mendoza",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

aplicar_estilos()


# ============================================================
# GOOGLE SHEETS
# ============================================================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

cliente_google = gspread.authorize(creds)

sheet = cliente_google.open_by_key(
    "1gZSTBtwx00MIh1b01rm2lDqBBjWnmA78o7agYh9zeG4"
).sheet1


# ============================================================
# CARGAR DATOS DEL DASHBOARD
# ============================================================

@st.cache_data(ttl=10)
def cargar_datos():

    registros = sheet.get_all_records()

    if len(registros) == 0:
        return pd.DataFrame()

    return pd.DataFrame(registros)


df = cargar_datos()


# ============================================================
# MODELO DE MACHINE LEARNING
# ============================================================

modelo = joblib.load("modelo_creditos.pkl")
scaler = joblib.load("scaler_creditos.pkl")


# ============================================================
# HEADER PRINCIPAL
# ============================================================

col_logo, col_info, col_fecha = st.columns([1,4,2])

with col_logo:

    st.markdown(
        """
        <div style='font-size:70px;text-align:center'>
        🏦
        </div>
        """,
        unsafe_allow_html=True
    )

with col_info:

    st.markdown(
        """
        <h1 style="color:#0057B8;
                   margin-bottom:0px;
                   font-size:42px;">
            BANCO MENDOZA
        </h1>

        <p style="font-size:18px;
                  color:#6b7280;
                  margin-top:-10px;">

        Sistema Inteligente de Evaluación Crediticia

        </p>

        <p style="font-size:15px;
                  color:#9CA3AF;">

        Machine Learning • Analítica • Inteligencia Artificial

        </p>
        """,
        unsafe_allow_html=True
    )

with col_fecha:

    st.metric(
        "Fecha",
        datetime.now().strftime("%d/%m/%Y")
    )

    st.metric(
        "Hora",
        datetime.now().strftime("%H:%M")
    )

st.markdown("---")
