import streamlit as st

def aplicar_estilos():

    st.markdown("""
<style>

/* ======================================================
BANCO MENDOZA
Sistema Inteligente de Evaluación Crediticia
======================================================*/

/* Importar fuente */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Fondo general */

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;

}

.stApp{

    background:#F3F8FD;

}

/* Ocultar elementos Streamlit */

#MainMenu{

    visibility:hidden;

}

footer{

    visibility:hidden;

}

header{

    visibility:hidden;

}

/* ==========================
HEADER
========================== */

.header{

    background:linear-gradient(90deg,#0057B8,#1E88E5);

    padding:28px;

    border-radius:18px;

    color:white;

    box-shadow:0px 8px 25px rgba(0,0,0,.15);

    margin-bottom:25px;

}

.header h1{

    font-size:38px;

    margin-bottom:5px;

    font-weight:700;

}

.header h4{

    font-weight:400;

    opacity:.9;

}

/* ==========================
CARDS
========================== */

.card{

    background:white;

    border-radius:18px;

    padding:22px;

    box-shadow:0 5px 18px rgba(0,0,0,.08);

    border:1px solid #EEF2F7;

    margin-bottom:20px;

}

/* ==========================
TÍTULOS
========================== */

.section-title{

    color:#0057B8;

    font-size:24px;

    font-weight:700;

    margin-bottom:15px;

}

/* ==========================
INPUTS
========================== */

input{

    border-radius:12px !important;

}

textarea{

    border-radius:12px !important;

}

div[data-baseweb="select"]{

    border-radius:12px;

}

/* ==========================
BOTONES
========================== */

.stButton>button{

    width:100%;

    background:#0057B8;

    color:white;

    border:none;

    border-radius:12px;

    height:55px;

    font-size:18px;

    font-weight:700;

    transition:.3s;

}

.stButton>button:hover{

    background:#00408D;

    transform:translateY(-2px);

}

/* ==========================
KPIs
========================== */

div[data-testid="metric-container"]{

    background:white;

    padding:20px;

    border-radius:18px;

    box-shadow:0px 4px 15px rgba(0,0,0,.08);

    border-left:6px solid #0057B8;

}

div[data-testid="metric-container"] label{

    color:#7A7A7A;

    font-weight:600;

}

div[data-testid="metric-container"] div{

    color:#0057B8;

}

/* ==========================
SUCCESS
========================== */

.stSuccess{

    border-radius:15px;

}

/* ==========================
WARNING
========================== */

.stWarning{

    border-radius:15px;

}

/* ==========================
INFO
========================== */

.stInfo{

    border-radius:15px;

}

/* ==========================
DATAFRAME
========================== */

.dataframe{

    border:none;

}

/* ==========================
SIDEBAR
========================== */

section[data-testid="stSidebar"]{

    background:#0B3B75;

}

section[data-testid="stSidebar"] *{

    color:white;

}

/* ==========================
PROGRESS
========================== */

.stProgress>div>div{

    background:#0057B8;

}

/* ==========================
EXPANDER
========================== */

.streamlit-expanderHeader{

    font-weight:600;

}

/* ==========================
SEPARADOR
========================== */

hr{

    border:1px solid #E6EEF7;

}

/* ==========================
TABLAS
========================== */

table{

    border-collapse:collapse;

}

thead tr{

    background:#0057B8;

    color:white;

}

tbody tr:nth-child(even){

    background:#F5F9FF;

}

/* ==========================
FOOTER
========================== */

.footer{

    text-align:center;

    color:#8A8A8A;

    margin-top:40px;

    font-size:14px;

}

</style>

""", unsafe_allow_html=True)
