import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ======================================================
# CONFIGURACIÓN
# ======================================================

st.set_page_config(
    page_title="Banco Mendoza",
    page_icon="🏦",
    layout="wide"
)

st_autorefresh(interval=10000, key="refresh")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSZEU4gn9FertCpntuqUc10Qij3o30n4cz1iPjZ6YwTGFibiKWNfIbjKxuEb7QnlqRoY7_643-yd0Q/pub?gid=0&single=true&output=csv"

# ======================================================
# ESTILOS
# ======================================================

st.markdown("""
<style>

.stApp{
    background:#F4F8FC;
}

.block-container{
    padding-top:1rem;
}

.kpi{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    border-left:6px solid #0057B8;
    text-align:center;
}

.kpi h3{
    color:#7A7A7A;
    margin-bottom:8px;
    font-size:16px;
}

.kpi h1{
    color:#0057B8;
    margin:0;
    font-size:38px;
}

.header{

background:linear-gradient(90deg,#0057B8,#2196F3);

padding:25px;

border-radius:20px;

color:white;

margin-bottom:25px;

box-shadow:0 10px 25px rgba(0,0,0,.15);

}

.header h1{

font-size:40px;

margin:0;

}

.header h4{

font-weight:400;

margin-top:5px;

}

</style>

""", unsafe_allow_html=True)

# ======================================================
# CARGAR DATOS
# ======================================================

df = pd.read_csv(CSV_URL)

numericas = [
    "Edad",
    "Ingresos",
    "Score",
    "Valor_Credito",
    "Plazo",
    "Probabilidad",
    "Capacidad_Pago"
]

for c in numericas:

    if c in df.columns:

        df[c] = (
            df[c]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        df[c] = pd.to_numeric(df[c], errors="coerce")

# ======================================================
# INDICADORES
# ======================================================

total = len(df)

aprobados = len(df[df["Resultado"].str.contains("APROBADO",na=False)])

rechazados = len(df[df["Resultado"].str.contains("RECHAZADO",na=False)])

revision = len(df[df["Resultado"].str.contains("REVIS",na=False)])

monto = df["Valor_Credito"].sum()

score = round(df["Score"].mean(),0)

prob = round(df["Probabilidad"].mean(),1)

capacidad = round(df["Capacidad_Pago"].mean(),1)

# ======================================================
# HEADER
# ======================================================

st.markdown(f"""

<div class="header">

<h1> BANCO MENDOZA</h1>

<h4>Sistema Inteligente de Evaluación Crediticia</h4>

Dashboard Ejecutivo · Actualización automática cada 10 segundos

</div>

""",unsafe_allow_html=True)

# ======================================================
# KPI
# ======================================================

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown(f"""

<div class="kpi">

<h3>Solicitudes</h3>

<h1>{total}</h1>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown(f"""

<div class="kpi">

<h3>Aprobados</h3>

<h1>{aprobados}</h1>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown(f"""

<div class="kpi">

<h3>Rechazados</h3>

<h1>{rechazados}</h1>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown(f"""

<div class="kpi">

<h3>En Revisión</h3>

<h1>{revision}</h1>

</div>

""",unsafe_allow_html=True)

st.write("")

c5,c6,c7,c8 = st.columns(4)

with c5:

    st.markdown(f"""

<div class="kpi">

<h3>Monto Solicitado</h3>

<h1>${monto:,.0f}</h1>

</div>

""",unsafe_allow_html=True)

with c6:

    st.markdown(f"""

<div class="kpi">

<h3>Score Promedio</h3>

<h1>{score}</h1>

</div>

""",unsafe_allow_html=True)

with c7:

    st.markdown(f"""

<div class="kpi">

<h3>Probabilidad</h3>

<h1>{prob}%</h1>

</div>

""",unsafe_allow_html=True)

with c8:

    st.markdown(f"""

<div class="kpi">

<h3>Capacidad Pago</h3>

<h1>{capacidad}%</h1>

</div>

""",unsafe_allow_html=True)

st.markdown("---")

# ======================================================
# DASHBOARD GRÁFICO
# ======================================================

st.subheader(" Indicadores Ejecutivos")

col1, col2 = st.columns(2)

# =====================================
# DONA
# =====================================

with col1:

    st.markdown("### 🥧 Resultado de Solicitudes")

    resultados = (
        df["Resultado"]
        .value_counts()
        .reset_index()
    )
    resultados.columns = [
        "Resultado",
        "Cantidad"
    ]

    fig = px.pie(
        resultados,
        names="Resultado",
        values="Cantidad",
        hole=0.65
    )

    fig.update_layout(
  
    height=430,
    margin=dict(
        l=10,
        r=10,
        t=0,
        b=10
    )
)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# VELOCÍMETRO
# =====================================

with col2:

    st.subheader("Probabilidad de aprobación")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=prob,
            number={"suffix": "%"},
            title={"text": " "},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1565C0"},
                "steps": [
                    {"range": [0, 40], "color": "#F44336"},
                    {"range": [40, 70], "color": "#FFC107"},
                    {"range": [70, 100], "color": "#4CAF50"},
                ]
            }
        )
    )

    fig.update_layout(
        height=370,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
