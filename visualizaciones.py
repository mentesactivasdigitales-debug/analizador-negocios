import plotly.express as px
import pandas as pd

def generar_grafico_contraste(total_pos, total_neg, filtro_actual):
    fig_data = pd.DataFrame({"Resultado": ["Satisfacción", "Fallas"], "Cantidad": [total_pos, total_neg]})
    alpha_pos = 1.0 if filtro_actual in ["TODOS", "POSITIVO"] else 0.15
    alpha_neg = 1.0 if filtro_actual in ["TODOS", "NEGATIVO"] else 0.15
    colores_rgba = [f'rgba(46, 204, 113, {alpha_pos})', f'rgba(231, 76, 60, {alpha_neg})']
    fig = px.pie(fig_data, values='Cantidad', names='Resultado', hole=0.5, color_discrete_sequence=colores_rgba)
    fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#1E1E1E', width=2)), sort=False)
    return fig

def generar_grafico_departamentos(df_quejas):
    if df_quejas.empty: return None
    df_cat = df_quejas['Departamento'].value_counts().reset_index()
    df_cat.columns = ['Departamento', 'Frecuencia']
    return px.bar(df_cat, x='Departamento', y='Frecuencia', title="Fallas por Departamento Operativo",
                  color='Frecuencia', color_continuous_scale='OrRd')

def generar_grafico_causa(df_frec):
    return px.bar(df_frec, x='Frecuencia', y='Problema', orientation='h', 
                  title="Top 10 Dolores del Cliente", color='Frecuencia', color_continuous_scale='Reds')
