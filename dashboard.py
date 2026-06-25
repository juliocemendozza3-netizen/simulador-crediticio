import streamlit as st
import pandas as pd
import gspread

from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Dashboard Banco Mendoza",
    layout="wide"
)

# Actualizar automáticamente cada 10 segundos
st_autorefresh(
    interval=10000,
    key="dashboard_refresh"
)

# ======================================================
# CONEXIÓN A GOOGLE SHEETS
# ======================================================

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

# ======================================================
# CARGAR DATOS
# ======================================================

@st.cache_data(ttl=5)
def cargar_datos():
    registros = sheet.get_all_records()
    return pd.DataFrame(registros)

df = cargar_datos()

# Convertir columnas numéricas
columnas_numericas = [
    "Edad",
    "Ingresos",
    "Score",
    "Valor_Credito",
    "Plazo",
    "Probabilidad",
    "Capacidad_Pago"
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# INDICADORES
# =========================

total_solicitudes = len(df)

aprobados = len(
    df[df["Resultado"].astype(str).str.contains("APROBADO", na=False)]
)

rechazados = len(
    df[df["Resultado"].astype(str).str.contains("RECHAZADO", na=False)]
)

monto_total = df["Valor_Credito"].fillna(0).sum()

score_promedio = round(
    df["Score"].fillna(0).mean(),
    0
)

prob_promedio = round(
    df["Probabilidad"].fillna(0).mean(),
    2
)

# =========================
# DASHBOARD
# =========================

st.title("📊 Dashboard Crediticio Banco Mendoza")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Solicitudes",
    total_solicitudes
)

c2.metric(
    "Aprobados",
    aprobados
)

c3.metric(
    "Rechazados",
    rechazados
)

c4.metric(
    "Monto Total",
    f"${monto_total:,.0f}"
)

c5.metric(
    "Probabilidad Promedio",
    f"{prob_promedio}%"
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Resultados")
    st.bar_chart(df["Resultado"].value_counts())

with col2:
    st.subheader("Score Crediticio")
    st.line_chart(df["Score"])

st.markdown("---")

st.subheader("Últimas Solicitudes")

st.dataframe(
    df,
    use_container_width=True
)
