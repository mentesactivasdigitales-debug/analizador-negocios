import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
import os

st.set_page_config(page_title="Intelligence Business Pro", layout="wide")

st.title("🚀 Consultor de Inteligencia de Mercado V5.9")
st.markdown("### Auditoría de Precisión Real - Maldonado")

# --- CARGA DE DATOS ---
st.sidebar.header("📥 Activos de Datos")
archivo_client = st.sidebar.file_uploader("Datos del CLIENTE", type=["xlsx", "csv"])
archivos_comp = st.sidebar.file_uploader("Benchmarks COMPETENCIA", type=["xlsx", "csv"], accept_multiple_files=True)

def auditoria_estricta(texto):
    if not isinstance(texto, str) or str(texto).strip() == "": return 0
    
    texto_limpio = str(texto).lower()

    # 1. LISTA DE SALVACIÓN
    palabras_positivas = ['rico', 'excelente', 'recomiendo', 'abundante', 'impecable', 'bueno','bien']

    if any(p in texto_limpio for p in palabras_positivas) and "no" not in texto_limpio.split(palabras_positivas[0])[0]:
        return 0

    # 2. Análisis de Sentimiento
    sentimiento = TextBlob(str(texto)).sentiment.polarity

    # 3. Diccionario de Fallas Reales
    palabras_queja = ['mala', 'fria','fría', 'tarda','demora', 'caro','pelo', 'quemada','cruda', 'sucio','cucaracha']
    tiene_queja_palabra = any(p in texto_limpio for p in palabras_queja)

    if tiene_queja_palabra and sentimiento < 0.1:
        return -1 
    return 0

if archivo_client:
    nombre_empresa = os.path.splitext(archivo_client.name)[0].upper()
    df_cliente = pd.read_excel(archivo_client) if archivo_client.name.endswith('xlsx') else pd.read_csv(archivo_client)
    
    columnas = list(df_cliente.columns)
    idx_def = columnas.index("Reseña") if "Reseña" in columnas else 0
    col_resena = st.selectbox("Columna analizada:", columnas, index=idx_def)

    # PROCESAMIENTO
    df_cliente['Resultado_Auditoria'] = df_cliente[col_resena].apply(auditoria_estricta)
    quejas_reales = df_cliente[df_cliente['Resultado_Auditoria'] == -1].copy()
    satisfaccion = df_cliente[df_cliente['Resultado_Auditoria'] == 0].copy()

    # --- MÉTRICAS DE NEGOCIO ---
    ticket = st.number_input("Ticket Promedio ($U)", value=800)
    n_quejas = len(quejas_reales)
    impacto_directo = n_quejas * ticket
    impacto_anual = impacto_directo * 12

    st.subheader(f"💰 Datos Cliente: {nombre_empresa}")
    st.markdown("#### Auditoría de Capital (Filtro de Quejas Reales)")

    c1, c2, c3 = st.columns(3)
    c1.metric("Quejas Operativas", f"{n_quejas}")

    porcentaje_falla = (n_quejas / len(df_cliente)) * 100 if len(df_cliente) > 0 else 0

    if porcentaje_falla > 15:
        estado, color = "CRÍTICO", "red"
    elif porcentaje_falla > 5:
        estado, color = "RIESGO", "orange"
    else:
        estado, color = "SALUDABLE", "green"

    c2.markdown(f"<h3 style='color:{color}; text-align:center;'>ESTADO: {estado}</h3>", unsafe_allow_html=True)
    c3.metric("Impacto Anual Proyectado", f"${impacto_anual:,.0f}")

    # --- GRÁFICOS ---
    st.subheader("📊 Visualización de Salud del Negocio")
    fig_data = pd.DataFrame({
        "Resultado": ["Satisfacción/Neutro", "Fallas Reales"],
        "Cantidad": [len(df_cliente) - n_quejas, n_quejas]
    })
    fig = px.pie(fig_data, values='Cantidad', names='Resultado', color_discrete_sequence=['#2ecc71', '#e74c3c'], hole=0.4)
    st.plotly_chart(fig, width='stretch')

    # --- NUEVA FUNCIÓN: BOTONES DE FILTRADO PROFESIONAL ---
    st.subheader("🎯 Explorador de Auditoría")
    
    # Inicialización del estado de filtro si no existe
    if 'filtro_actual' not in st.session_state:
        st.session_state.filtro_actual = "TODOS"

    col_f1, col_f2, col_f3 = st.columns(3)
    
    if col_f1.button("✅ Ver Positivos / Neutros", use_container_width=True):
        st.session_state.filtro_actual = "POSITIVO"
    if col_f2.button("❌ Ver Fallas Reales", use_container_width=True):
        st.session_state.filtro_actual = "NEGATIVO"
    if col_f3.button("📋 Ver Todo el Archivo", use_container_width=True):
        st.session_state.filtro_actual = "TODOS"

    # --- EVIDENCIA BASADA EN FILTRO ---
    st.markdown(f"**Vista seleccionada:** {st.session_state.filtro_actual}")
    
    if st.session_state.filtro_actual == "NEGATIVO":
        if not quejas_reales.empty:
            st.dataframe(quejas_reales[[col_resena]], width='stretch')
        else:
            st.success("No se encontraron fallas críticas.")
            
    elif st.session_state.filtro_actual == "POSITIVO":
        if not satisfaccion.empty:
            st.dataframe(satisfaccion[[col_resena]], width='stretch')
        else:
            st.info("No hay registros positivos en esta auditoría.")
            
    else:
        st.dataframe(df_cliente[[col_resena, 'Resultado_Auditoria']], width='stretch')

else:
    st.info("Cargue los archivos para iniciar la auditoría profesional.")
