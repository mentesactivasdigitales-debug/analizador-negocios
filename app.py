import streamlit as st
import pandas as pd
import os
import auditoria_pro as engine
import visualizaciones as visuals
import plotly.express as px

st.set_page_config(page_title="Intelligence Business Pro", layout="wide")
st.title("🚀 Consultor de Inteligencia Multirrubro V7.0")

# --- SIDEBAR: SELECTOR DE NICHO ---
st.sidebar.header("🎯 Configuración de Consultoría")
rubro_seleccionado = st.sidebar.selectbox(
    "Seleccione el Ramo Comercial:", 
    ["Gastronomía", "Hotelería", "Salud/Clínicas", "Gimnasios"] # Rubro añadido
)

st.sidebar.markdown("---")
# Mantenemos la lógica de divisas profesional
st.sidebar.header("💱 Configuración de Divisas")
tasa_cambio = st.sidebar.number_input("Tipo de Cambio (1 USD a UYU):", value=40.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("📥 Activos de Datos")
archivo_client = st.sidebar.file_uploader(f"Datos del {rubro_seleccionado.upper()}", type=["xlsx", "csv"])

if archivo_client:
    nombre_empresa = os.path.splitext(archivo_client.name)[0].upper()
    df = pd.read_excel(archivo_client) if archivo_client.name.endswith('xlsx') else pd.read_csv(archivo_client)
    
    columnas = list(df.columns)
    col_resena = st.selectbox("Columna de Reseñas:", columnas, index=columnas.index("Reseña") if "Reseña" in columnas else 0)

    # PROCESAMIENTO DINÁMICO
    df['Resultado_Auditoria'] = df[col_resena].apply(lambda x: engine.auditoria_estricta(x, rubro_seleccionado))
    quejas = df[df['Resultado_Auditoria'] == -1].copy()
    quejas['Departamento'] = quejas[col_resena].apply(lambda x: engine.categorizar_falla(x, rubro_seleccionado))
    satisfaccion = df[df['Resultado_Auditoria'] == 0].copy()

    # MÉTRICAS BIMONEDA
    st.subheader("💰 Evaluación de Impacto Financiero")
    ticket_uyu = st.number_input("Valor Promedio de Membresía/Transacción ($U):", value=2500)
    
    impacto_anual_uyu = (len(quejas) * ticket_uyu) * 12
    impacto_anual_usd = impacto_anual_uyu / tasa_cambio
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Fallas Detectadas", len(quejas))
    c2.metric("Pérdida Anual ($U)", f"$ {impacto_anual_uyu:,.0f}")
    c3.metric("Pérdida Anual (US$)", f"US$ {impacto_anual_usd:,.0f}")

    # ... [LÓGICA DE GRÁFICOS Y TABLAS SE MANTIENE IGUAL] ...

    # --- SECCIÓN DE CIERRE Y REPORTES DINÁMICOS ---
    st.markdown("---")
    if not quejas.empty:
        st.subheader("📝 Resumen Ejecutivo de Consultoría")
        falla_principal = quejas['Departamento'].value_counts().idxmax()
        porcentaje_fallas = (len(quejas) / len(df)) * 100
        
        # Diccionario actualizado con narrativa de gimnasios
        vocabulario = {
            "Gastronomía": "pérdida de recurrencia de comensales y erosión de marca.",
            "Hotelería": "deterioro del prestigio de alojamiento y riesgo en la tasa de ocupación.",
            "Salud/Clínicas": "quiebre de confianza en la atención y riesgo de deserción de pacientes.",
            "Gimnasios": "cancelación masiva de membresías y debilitamiento del índice de retención de socios."
        }
        
        narrativa_especifica = vocabulario.get(rubro_seleccionado, "riesgo operativo general.")

        plantilla = f"""
        *AUDITORÍA ESTRATÉGICA PARA {nombre_empresa}:*

        Se han identificado los siguientes puntos críticos que impactan la rentabilidad:

        1. **Impacto Financiero Proyectado:** - Moneda Local: **$ {impacto_anual_uyu:,.0f} UYU**
           - Divisa: **US$ {impacto_anual_usd:,.0f} USD**
        2. **Cuello de Botella Operativo:** El área de **{falla_principal}** presenta la mayor incidencia crítica.
        3. **Riesgo Reputacional:** Un **{porcentaje_fallas:.1f}%** de las interacciones contienen indicadores de **{narrativa_especifica}**

        *RECOMENDACIÓN:* Acción inmediata sobre los activos de **{falla_principal}** para frenar la fuga de capital.
        """
        st.info(plantilla)

        # [BOTÓN DE DESCARGA SE MANTIENE IGUAL]
