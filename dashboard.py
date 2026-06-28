import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Dashboard Banco Mendoza",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>

div[data-testid="stPlotlyChart"]{

    background:white;

    border:1px solid #D9D9D9;

    border-radius:18px;

    padding:20px;

    margin-bottom:25px;

    overflow:hidden;

    box-shadow:0 4px 12px rgba(0,0,0,.10);

}

</style>
""", unsafe_allow_html=True)

st_autorefresh(

    interval=10000,

    key="dashboard_refresh"

)

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSZEU4gn9FertCpntuqUc10Qij3o30n4cz1iPjZ6YwTGFibiKWNfIbjKxuEb7QnlqRoY7_643-yd0Q/pub?gid=0&single=true&output=csv"

# =========================
# CARGAR DATOS
# =========================

df = pd.read_csv(CSV_URL)

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

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

# =========================
# INDICADORES
# =========================

total_solicitudes = len(df)

aprobados = len(

    df[

        df["Resultado"]

        .astype(str)

        .str.contains("APROBADO", na=False)

    ]

)

rechazados = len(

    df[

        df["Resultado"]

        .astype(str)

        .str.contains("RECHAZADO", na=False)

    ]

)

revision = len(

    df[

        df["Resultado"]

        .astype(str)

        .str.contains("REVIS", na=False)

    ]

)

monto_total = df["Valor_Credito"].sum()

score_promedio = round(df["Score"].mean(),0)

prob_promedio = round(df["Probabilidad"].mean(),1)

capacidad = round(df["Capacidad_Pago"].mean(),1)

# =====================================================
# ENCABEZADO
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#0D47A1,#1976D2);
padding:28px;
border-radius:18px;
color:white;
box-shadow:0 8px 20px rgba(0,0,0,.15);
">

<h1 style="margin:0;">
BANCO MENDOZA
</h1>

<h3 style="margin-top:8px;font-weight:400;">
Sistema Inteligente de Evaluación Crediticia
</h3>

<p style="margin-top:10px;">
Dashboard Ejecutivo • Actualización automática
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# TARJETAS KPI
# =====================================================

c1, c2, c3, c4 = st.columns(4)

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
    "En Revisión",
    revision
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Monto Total",
    f"${monto_total:,.0f}"
)

c6.metric(
    "Score Promedio",
    score_promedio
)

c7.metric(
    "Probabilidad",
    f"{prob_promedio}%"
)

c8.metric(
    "Capacidad Pago",
    f"{capacidad}%"
)

st.markdown("---")
# =====================================================
# INDICADORES EJECUTIVOS
# =====================================================

graf1, graf2 = st.columns(2)

# =====================================================
# GRÁFICO DONUT
# =====================================================

with graf1:

    st.subheader("Resultado de Solicitudes")

    resultados = (
        df["Resultado"]
        .value_counts()
        .reset_index()
    )

    resultados.columns = ["Resultado", "Cantidad"]

    colores = []

    for r in resultados["Resultado"]:

        texto = str(r).upper()

        if "APROBADO" in texto:
            colores.append("#2E7D32")

        elif "RECHAZADO" in texto:
            colores.append("#D32F2F")

        else:
            colores.append("#FBC02D")

    fig = go.Figure(

        data=[

            go.Pie(

                labels=resultados["Resultado"],

                values=resultados["Cantidad"],

                hole=0.60,

                marker=dict(
                    colors=colores
                )

            )

        ]

    )

fig.update_layout(

    showlegend=False,

    height=420,

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=40
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)
# =====================================================
# GRÁFICO DE BARRAS
# =====================================================

with graf2:

    st.subheader("📊 Estado de las Solicitudes")

    estado = pd.DataFrame({

        "Estado":[
            "Aprobados",
            "Rechazados",
            "En Revisión"
        ],

        "Cantidad":[
            aprobados,
            rechazados,
            revision
        ]

    })

    fig = px.bar(

        estado,

        x="Estado",

        y="Cantidad",

        color="Estado",

        text="Cantidad",

        color_discrete_map={

            "Aprobados":"#2E7D32",

            "Rechazados":"#D32F2F",

            "En Revisión":"#FBC02D"

        }

    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(

    showlegend=False,

    height=380,

    margin=dict(
        l=40,
        r=20,
        t=20,
        b=40
    ),

    yaxis=dict(
        automargin=True
    ),

    xaxis=dict(
        automargin=True
    )

)
# =====================================================
# SEGUNDA FILA DE GRÁFICOS
# =====================================================

graf3, graf4 = st.columns(2)

# =====================================================
# VELOCÍMETRO
# =====================================================

with graf3:

    st.subheader("Probabilidad Promedio")

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=prob_promedio,

            number={"suffix":"%"},

            title={"text":"Nivel de aprobación"},

            gauge={

                "axis":{"range":[0,100]},

                "bar":{"color":"#1565C0"},

                "steps":[

                    {
                        "range":[0,40],
                        "color":"#D32F2F"
                    },

                    {
                        "range":[40,70],
                        "color":"#FBC02D"
                    },

                    {
                        "range":[70,100],
                        "color":"#2E7D32"
                    }

                ]

            }

        )

    )

    fig.update_layout(
        height=380
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # =====================================================
# EVOLUCIÓN DEL SCORE CREDITICIO
# =====================================================

with graf4:

    st.subheader("📈 Evolución del Score Crediticio")

    fig = px.line(

        df,

        y="Score",

        markers=True

    )

    fig.update_traces(

        line=dict(
            color="#1565C0",
            width=3
        ),

        marker=dict(
            size=8
        )

    )

    fig.update_layout(

        height=380,

        xaxis_title="Solicitudes",

        yaxis_title="Score",

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
    

# =====================================================
# TABLA
# =====================================================

st.markdown("---")

st.subheader("Últimas Solicitudes")

st.dataframe(

    df.sort_values(

        by="Fecha",

        ascending=False

    ),

    use_container_width=True

)
