import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analizador de Negocios Pro", page_icon="📈")

st.title("🚀 Analizador de Negocios Pro (V3)")

archivo = st.file_uploader("Sube tu archivo Excel o CSV", type=['csv', 'xlsx'])

if archivo:
    try:
        df = pd.read_excel(archivo) if archivo.name.endswith('xlsx') else pd.read_csv(archivo)
        st.success("✅ Archivo cargado")
        
        columna = st.selectbox("¿En qué columna están las reseñas?", df.columns)

        if st.button("Generar Informe Profesional"):
            # DICCIONARIO DE SENTIMIENTOS (El activo real)
            positivas = ['excelente', 'bueno', 'buena', 'mejor', 'encanto', 'encantó', 'rico', 'delicioso', 'amable', 'gracias', 'recomiendo', 'limpio', 'rapido', 'rápido']
            negativas = ['malo', 'mala', 'pesimo', 'pésimo', 'sucio', 'tarde', 'caro', 'frio', 'frío', 'mal', 'peor', 'horrible', 'nunca', 'asco', 'atencion', 'atención']

            def clasificar_espanol(texto):
                texto = str(texto).lower()
                # Sumamos puntos por palabras encontradas
                puntos_pos = sum(1 for p in positivas if p in texto)
                puntos_neg = sum(1 for p in negativas if p in texto)
                
                if puntos_pos > puntos_neg: return "🟢 Positivo"
                elif puntos_neg > puntos_pos: return "🔴 Negativo"
                else: return "🟡 Neutro"

            df['Sentimiento'] = df[columna].apply(clasificar_espanol)
            
            # DISEÑO DE REPORTE PARA EL CLIENTE
            total = len(df)
            pos = len(df[df['Sentimiento'] == "🟢 Positivo"])
            neg = len(df[df['Sentimiento'] == "🔴 Negativo"])
            neu = len(df[df['Sentimiento'] == "🟡 Neutro"])

            col1, col2, col3 = st.columns(3)
            col1.metric("Reseñas Totales", total)
            col2.metric("Clientes Felices", f"{pos}")
            col3.metric("Clientes Insatisfechos", f"{neg}")

            # GRÁFICA PROFESIONAL
            st.write("### 📊 Balance de Opiniones")
            conteo = df['Sentimiento'].value_counts()
            st.bar_chart(conteo)

            # LISTA DE DETALLES
            with st.expander("Ver detalle de cada comentario"):
                st.table(df[[columna, 'Sentimiento']])

            # BOTÓN DE DESCARGA (Para que el cliente te pague por el archivo)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📩 Descargar Informe para el Cliente", csv, "reporte_final.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {e}")