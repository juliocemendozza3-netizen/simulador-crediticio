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

if not df.empty:

    df = df.rename(columns={
        "Resultado": "decision_final",
        "Valor_Credito": "valor_credito",
        "Score": "score",
        "Probabilidad": "prob",
        "Capacidad_Pago": "capacidad_pago"
    })

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

# ============================================================
# DASHBOARD EJECUTIVO
# ============================================================

if len(df) > 0:

    total_solicitudes = len(df)

    aprobados = len(df[df["decision_final"].str.contains("APROBADO", case=False)])

    rechazados = len(df[df["decision_final"].str.contains("RECHAZADO", case=False)])

    revision = len(df[df["decision_final"].str.contains("REVIS", case=False)])

    monto_total = df["valor_credito"].sum()

    score_promedio = df["score"].mean()

    prob_promedio = df["prob"].mean()

    capacidad_promedio = df["capacidad_pago"].mean()

else:

    total_solicitudes = 0
    aprobados = 0
    rechazados = 0
    revision = 0
    monto_total = 0
    score_promedio = 0
    prob_promedio = 0
    capacidad_promedio = 0


st.markdown("## 📊 Dashboard Ejecutivo")


kpi1,kpi2,kpi3,kpi4 = st.columns(4)

with kpi1:

    st.metric(
        "Solicitudes",
        f"{total_solicitudes}"
    )

with kpi2:

    st.metric(
        "Aprobados",
        f"{aprobados}"
    )

with kpi3:

    st.metric(
        "Rechazados",
        f"{rechazados}"
    )

with kpi4:

    st.metric(
        "En Revisión",
        f"{revision}"
    )



kpi5,kpi6,kpi7,kpi8 = st.columns(4)

with kpi5:

    st.metric(
        "Monto Solicitado",
        f"${monto_total:,.0f}"
    )

with kpi6:

    st.metric(
        "Score Promedio",
        f"{score_promedio:.0f}"
    )

with kpi7:

    st.metric(
    "Probabilidad",
    f"{prob_promedio:.1f}%"
)

with kpi8:

    st.metric(
        "Capacidad Pago",
        f"{capacidad_promedio:.1f}%"
    )


st.markdown("---")

st.markdown("## 👤 Información del Cliente")

col1,col2 = st.columns(2)

with col1:

    edad = st.number_input(
        "Edad",
        18,
        100,
        30
    )

    ingresos = st.number_input(
        "Ingresos Mensuales",
        min_value=0,
        step=100000
    )

    score = st.number_input(
        "Score Crediticio",
        300,
        850,
        650
    )

    prestamos = st.number_input(
        "Préstamos Previos",
        0,
        20,
        0
    )

    antiguedad = st.number_input(
        "Antigüedad Laboral",
        0,
        40,
        5
    )

with col2:

    tipo_contrato = st.selectbox(
        "Tipo Contrato",
        [
            "Indefinido",
            "Independiente",
            "Temporal"
        ]
    )

    vivienda = st.selectbox(
        "Vivienda Propia",
        [
            "Sí",
            "No"
        ]
    )

    historial_mora = st.selectbox(
        "Historial Mora",
        [
            "Ninguna",
            "Ocasional"
        ]
    )

    nivel_educativo = st.selectbox(
        "Nivel Educativo",
        [
            "Tecnico",
            "Profesional",
            "Posgrado"
        ]
    )

    estado_civil = st.selectbox(
        "Estado Civil",
        [
            "Casado",
            "Soltero",
            "Union Libre"
        ]
    )

st.markdown("---")
