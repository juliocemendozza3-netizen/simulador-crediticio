import streamlit as st

def aplicar_estilos():

    st.markdown("""
    <style>

    /* ==========================
       FONDO GENERAL
    ========================== */

    .stApp{
        background-color:#F3F8FF;
    }

    /* ==========================
       TÍTULO
    ========================== */

    .titulo-principal{
        font-size:42px;
        font-weight:700;
        color:#0A4FAF;
        margin-bottom:5px;
    }

    .subtitulo{
        color:#5D6D7E;
        font-size:18px;
        margin-top:-10px;
    }

    /* ==========================
       TARJETAS
    ========================== */

    .card{

        background:white;

        padding:25px;

        border-radius:18px;

        box-shadow:0px 6px 20px rgba(0,0,0,.10);

        margin-bottom:20px;

    }

    /* ==========================
       BOTONES
    ========================== */

    .stButton>button{

        width:100%;

        background:#0B5ED7;

        color:white;

        border:none;

        border-radius:12px;

        height:55px;

        font-size:18px;

        font-weight:bold;

    }

    .stButton>button:hover{

        background:#0849A3;

        color:white;

    }

    /* ==========================
       INPUTS
    ========================== */

    input{

        border-radius:10px !important;

    }

    /* ==========================
       MÉTRICAS
    ========================== */

    div[data-testid="metric-container"]{

        background:white;

        border-radius:18px;

        padding:15px;

        box-shadow:0px 4px 15px rgba(0,0,0,.08);

    }

    </style>

    """, unsafe_allow_html=True)
