import streamlit as st
import pandas as pd
import joblib

# =========================
# CARGA DEL MODELO
# =========================

modelo = joblib.load("modelo_creditos.pkl")
scaler = joblib.load("scaler_creditos.pkl")

# =========================
# INTERFAZ
# =========================

st.title("🏦 Simulador Crediticio Inteligente")

st.write(
    "Evaluación basada en Machine Learning, score crediticio y capacidad de pago."
)

# =========================
# DATOS CLIENTE
# =========================

st.subheader("👤 Información del Cliente")

edad = st.number_input(
    "Edad",
    min_value=18,
    max_value=100,
    value=18
)

ingresos = st.number_input(
    "Ingresos Mensuales ($)",
    min_value=0,
    value=0,
    step=100000
   ) 
score = st.number_input(
    "Score Crediticio",
    min_value=300,
    max_value=850,
    value=300,
    key="score"
)

prestamos = st.number_input(
    "Préstamos Previos",
    min_value=0,
    value=0,
    key="prestamos"
)

antiguedad = st.number_input(
    "Antigüedad Laboral (años)",
    min_value=0,
    value=0,
    key="antiguedad"
)

# =========================
# INFORMACIÓN ADICIONAL
# =========================

st.subheader("📋 Información Adicional")

tipo_contrato = st.selectbox(
    "Tipo de Contrato",
    ["Indefinido", "Independiente", "Temporal"]
)

vivienda = st.selectbox(
    "Vivienda Propia",
    ["Sí", "No"]
)

historial_mora = st.selectbox(
    "Historial de Mora",
    ["Ninguna", "Ocasional"]
)

nivel_educativo = st.selectbox(
    "Nivel Educativo",
    ["Tecnico", "Profesional", "Posgrado"]
)

estado_civil = st.selectbox(
    "Estado Civil",
    ["Casado", "Soltero", "Union Libre"]
)

# =========================
# DATOS CRÉDITO
# =========================

st.subheader("💰 Información del Crédito")

valor_credito = st.number_input(
    "Valor Solicitado ($)",
    min_value=1000000,
    value=1000000,
    step=1000000,
    key="valor_credito"
)

plazo = st.number_input(
    "Plazo (Meses)",
    min_value=6,
    max_value=120,
    value=12,
    key="plazo"
)

# =========================
# EVALUACIÓN
# =========================

if st.button("✅ Evaluar Crédito"):

    if ingresos <= 0:
        st.error("Debe ingresar ingresos mayores a cero.")
        st.stop()

    # Variables dummy

    tipo_independiente = 1 if tipo_contrato == "Independiente" else 0
    tipo_temporal = 1 if tipo_contrato == "Temporal" else 0

    vivienda_si = 1 if vivienda == "Sí" else 0

    mora_ninguna = 1 if historial_mora == "Ninguna" else 0
    mora_ocasional = 1 if historial_mora == "Ocasional" else 0

    edu_posgrado = 1 if nivel_educativo == "Posgrado" else 0
    edu_profesional = 1 if nivel_educativo == "Profesional" else 0
    edu_tecnico = 1 if nivel_educativo == "Tecnico" else 0

    civil_soltero = 1 if estado_civil == "Soltero" else 0
    civil_union = 1 if estado_civil == "Union Libre" else 0

    cliente = pd.DataFrame({
        "Edad": [edad],
        "Ingresos_Mensuales": [ingresos],
        "Score_Crediticio": [score],
        "Prestamos_Previos": [prestamos],
        "Antiguedad_Laboral": [antiguedad],

        "Tipo_Contrato_Independiente": [tipo_independiente],
        "Tipo_Contrato_Temporal": [tipo_temporal],

        "Vivienda_Propia_Si": [vivienda_si],

        "Historial_Mora_Ninguna": [mora_ninguna],
        "Historial_Mora_Ocasional": [mora_ocasional],

        "Nivel_Educativo_Posgrado": [edu_posgrado],
        "Nivel_Educativo_Profesional": [edu_profesional],
        "Nivel_Educativo_Tecnico": [edu_tecnico],

        "Estado_Civil_Soltero": [civil_soltero],
        "Estado_Civil_Union Libre": [civil_union]
    })

    # Modelo ML

    cliente_scaled = scaler.transform(cliente)

    probabilidad = modelo.predict_proba(cliente_scaled)

    prob = round(probabilidad[0][1] * 100, 2)

    # Capacidad de pago

    tasa = 0.015

    cuota = (
        valor_credito
        * (tasa * (1 + tasa) ** plazo)
        / (((1 + tasa) ** plazo) - 1)
    )

    capacidad_pago = (cuota / ingresos) * 100

    # Semáforo

    if capacidad_pago < 35:
        semaforo = "🟢 VIABLE"
    elif capacidad_pago <= 45:
        semaforo = "🟡 REVISAR"
    else:
        semaforo = "🔴 NO VIABLE"

    # Decisión final

    if score < 500:
        decision_final = "🔴 RECHAZADO"
        motivo = "Score crediticio inferior a 500"

    elif capacidad_pago > 45:
        decision_final = "🔴 RECHAZADO"
        motivo = "Capacidad de pago insuficiente"

    elif score < 550:
        decision_final = "🟡 REVISIÓN MANUAL"
        motivo = "Score crediticio intermedio"

    elif prob >= 70:
        decision_final = "🟢 APROBADO"
        motivo = "Cumple criterios de riesgo y capacidad de pago"

    elif prob >= 40:
        decision_final = "🟡 REVISIÓN MANUAL"
        motivo = "Resultado intermedio del modelo"

    else:
        decision_final = "🔴 RECHAZADO"
        motivo = "Resultado desfavorable del modelo"

    # Resultados

    st.markdown("---")
    st.subheader("📊 Resultado de la Evaluación")

    st.success(
        f"Probabilidad ML: {prob}%"
    )

    st.success(
    f"Probabilidad de aprobación: {prob}%"
    )

st.progress(int(prob))
   
st.info(
        f"Cuota estimada: ${cuota:,.0f}"
    )

    
st.info(
        f"Capacidad de pago: {capacidad_pago:.2f}%"
    )

    
st.warning(
        f"Semáforo financiero: {semaforo}"
    )

    
st.markdown(f"## {decision_final}")

    
st.write(f"**Motivo:** {motivo}")

st.markdown("---")

if st.button("🔄 Nueva Consulta"):
    st.rerun()
    
