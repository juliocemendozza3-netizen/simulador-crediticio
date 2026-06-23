import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Banco Mendoza",
    layout="wide"
)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSZEU4gn9FertCpntuqUc10Qij3o30n4cz1iPjZ6YwTGFibiKWNfIbjKxuEb7QnlqRoY7_643-yd0Q/pub?gid=0&single=true&output=csv"

df = pd.read_csv(CSV_URL)

st.title("📊 Dashboard Crediticio Banco Mendoza")

total_solicitudes = len(df)

aprobados = len(
    df[df["Resultado"].str.contains("APROBADO", na=False)]
)

rechazados = len(
    df[df["Resultado"].str.contains("RECHAZADO", na=False)]
)

monto_total = df["Valor_Credito"].sum()

score_promedio = round(df["Score"].mean(), 0)

prob_promedio = round(df["Probabilidad"].mean(), 2)

c1,c2,c3,c4,c5,c6 = st.columns(6)

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
    "Score Promedio",
    score_promedio
)

c6.metric(
    "Probabilidad Promedio",
    f"{prob_promedio}%"
)

st.markdown("---")

st.subheader("Resultado de Créditos")

st.bar_chart(
    df["Resultado"].value_counts()
)

st.subheader("Probabilidad de Aprobación")

st.line_chart(
    df["Probabilidad"]
)

st.subheader("Score Crediticio")

st.line_chart(
    df["Score"]
)

st.subheader("Últimas Solicitudes")

st.dataframe(df)
