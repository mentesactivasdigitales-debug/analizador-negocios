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
    palabras_positivas = ['rico', 'excelente','recomiendo', 'abundante','impecable', 'bueno','bien']
    if any(p in texto_limpio for p in palabras_positivas) and "no" not in texto_limpio.split(palabras_positivas[0])[0]:
        return 0
    sentimiento = TextBlob(str(texto)).sentiment.polarity
    palabras_queja = ['mala', 'fria','fría','tarda','demora','caro','pelo','quemada','cruda','sucio','cucaracha']
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
    impacto_anual = (n_quejas * ticket) * 12

    st.subheader(f"💰 Datos Cliente: {nombre_empresa}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Quejas Operativas", f"{n_quejas}")
    
    porcentaje_falla = (n_quejas / len(df_cliente)) * 100 if len(df_cliente) > 0 else 0
    estado, color = ("CRÍTICO", "red") if porcentaje_falla > 15 else (("RIESGO", "orange") if porcentaje_falla > 5 else ("SALUDABLE", "green"))
    
    c2.markdown(f"<h3 style='color:{color}; text-align:center;'>ESTADO: {estado}</h3>", unsafe_allow_html=True)
    c3.metric("Impacto Anual Proyectado", f"${impacto_anual:,.0f}")

    # --- SISTEMA DE FILTRADO DINÁMICO ---
    st.subheader("🎯 Explorador de Auditoría")
    if 'filtro_actual' not in st.session_state:
        st.session_state.filtro_actual = "TODOS"

    col_f1, col_f2, col_f3 = st.columns(3)
    if col_f1.button("✅ Ver Positivos / Neutros", use_container_width=True):
        st.session_state.filtro_actual = "POSITIVO"
    if col_f2.button("❌ Ver Fallas Reales", use_container_width=True):
        st.session_state.filtro_actual = "NEGATIVO"
    if col_f3.button("📋 Ver Todo el Archivo", use_container_width=True):
        st.session_state.filtro_actual = "TODOS"

    if st.session_state.filtro_actual == "NEGATIVO":
        df_visual = quejas_reales
    elif st.session_state.filtro_actual == "POSITIVO":
        df_visual = satisfaccion
    else:
        df_visual = df_cliente

    # --- GRÁFICO DE CONTRASTE ESTADÍSTICO ---
    st.subheader(f"📊 Contexto de Auditoría: {st.session_state.filtro_actual}")
    
    # El gráfico SIEMPRE muestra el total para dar contraste, pero resalta lo seleccionado
    val_neg_total = len(quejas_reales)
    val_pos_total = len(satisfaccion)
    
    fig_data = pd.DataFrame({
        "Resultado": ["Satisfacción", "Fallas"],
        "Cantidad": [val_pos_total, val_neg_total]
    })
    
    # Lógica de opacidad para enfoque visual profesional
    op_pos = 1.0 if st.session_state.filtro_actual in ["TODOS", "POSITIVO"] else 0.15
    op_neg = 1.0 if st.session_state.filtro_actual in ["TODOS", "NEGATIVO"] else 0.15

    fig = px.pie(
        fig_data, 
        values='Cantidad', 
        names='Resultado',
        color='Resultado', 
        color_discrete_map={"Satisfacción": "#2ecc71", "Fallas": "#e74c3c"},
        hole=0.5
    )
    
    # Aplicamos contraste mediante actualización de trazos
    fig.update_traces(
        marker=dict(opacity=[op_pos, op_neg], line=dict(color='#FFFFFF', width=2)),
        textinfo='percent+label',
        hoverinfo='label+value'
    )

    # KPI Central con el volumen total de datos
    fig.add_annotation(
        text=f"Total<br>{len(df_cliente)}",
        showarrow=False,
        font=dict(size=20, color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- EVIDENCIA ---
    st.markdown(f"**Detalle de Registros Filtrados:**")
    if not df_visual.empty:
        st.dataframe(df_visual[[col_resena]], width='stretch')
    else:
        st.info(f"No hay registros en la categoría: {st.session_state.filtro_actual}")

else:
    st.info("Cargue los archivos para iniciar la auditoría profesional.")
