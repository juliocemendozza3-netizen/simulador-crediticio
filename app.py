import streamlit as st
import pandas as pd
import joblib

# Cargar modelo y scaler
modelo = joblib.load("modelo_creditos.pkl")
scaler = joblib.load("scaler_creditos.pkl")

st.title("🏦 Simulador Crediticio")

st.write("Ingrese los datos del cliente")

edad = st.number_input("Edad", min_value=18, max_value=100, value=30)

ingresos = st.number_input(
    "Ingresos mensuales",
    min_value=0,
    value=5000000
)

score = st.number_input(
    "Score crediticio",
    min_value=300,
    max_value=850,
    value=650
)

prestamos = st.number_input(
    "Préstamos previos",
    min_value=0,
    value=0
)

antiguedad = st.number_input(
    "Antigüedad laboral (años)",
    min_value=0,
    value=5
)

if st.button("Evaluar Crédito"):

    cliente = pd.DataFrame({
        "Edad": [edad],
        "Ingresos_Mensuales": [ingresos],
        "Score_Crediticio": [score],
        "Prestamos_Previos": [prestamos],
        "Antiguedad_Laboral": [antiguedad],
        "Tipo_Contrato_Independiente": [0],
        "Tipo_Contrato_Temporal": [0],
        "Vivienda_Propia_Si": [1],
        "Historial_Mora_Ninguna": [1],
        "Historial_Mora_Ocasional": [0],
        "Nivel_Educativo_Posgrado": [0],
        "Nivel_Educativo_Profesional": [1],
        "Nivel_Educativo_Tecnico": [0],
        "Estado_Civil_Soltero": [0],
        "Estado_Civil_Union Libre": [1]
    })

    cliente_scaled = scaler.transform(cliente)

    prediccion = modelo.predict(cliente_scaled)

    probabilidad = modelo.predict_proba(cliente_scaled)

    prob = round(probabilidad[0][1] * 100, 2)

    if prediccion[0] == 1:
        decision = "APROBADO"
    else:
        decision = "RECHAZADO"

    if prob >= 70:
        riesgo = "BAJO"
    elif prob >= 40:
        riesgo = "MEDIO"
    else:
        riesgo = "ALTO"

    st.success(f"Probabilidad: {prob}%")
    st.info(f"Riesgo: {riesgo}")
    st.warning(f"Decisión: {decision}")
