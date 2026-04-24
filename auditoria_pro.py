import pandas as pd
from textblob import TextBlob
import re
from collections import Counter

# Diccionario Maestro de Consultoría Actualizado
DICCIONARIOS = {
    "Gastronomía": {
        "categorias": {
            'COCINA': ['cruda','quemada','fria','fría','gusto','sabor','pelo','comida','pizzas','pastas','salado'],
            'SERVICIO': ['tarda','demora','atención','atencion','mozo','espera','recepción','atendieron','maltrato'],
            'PRECIO/VALOR': ['caro','precio','calidad','estafa','cobraron','carísimo','robo'],
            'HIGIENE/AMB': ['sucio','baño','olor','ruido','limpieza','cucaracha','incómodo','mosca']
        },
        "quejas": ['mala', 'fria','tarda','caro','sucio','pésimo','peores','malísima']
    },
    "Hotelería": {
        "categorias": {
            'LIMPIEZA': ['sábanas','sabanas','sucio','baño','toallas','olor','mugre','limpieza'],
            'CONFORT': ['ruido','cama','almohada','aire','frío','calor','colchón','viejo'],
            'RECEPCIÓN': ['check-in','atención','recepcionista','demora','espera','trato','maleta'],
            'SERVICIOS': ['desayuno','wifi','piscina','gym','estacionamiento','pobre','malo']
        },
        "quejas": ['sucio', 'ruido','malo','pésimo','caro','viejo','decepcionante']
    },
    "Salud/Clínicas": {
        "categorias": {
            'MÉDICO': ['diagnóstico','trato','profesional','médico','doctor','atención','revisó'],
            'ADMINISTRACIÓN': ['turno','espera','tarda','secretaria','teléfono','cobro','orden'],
            'INSTALACIONES': ['sucio','sala','asiento','baño','frío','calor','olor'],
            'URGENCIAS': ['demora','prioridad','atendieron','tarde','espera']
        },
        "quejas": ['espera', 'tarde','maltrato','sucio','pésimo','caro','error']
    },
    "Gimnasios": {
        "categorias": {
            'EQUIPAMIENTO': ['máquina','mancuerna', 'roto','mantenimiento', 'polea','cinta', 'oxidado','pesos', 'bicicleta'],
            'HIGIENE': ['sucio','olor', 'baño','vestuario', 'ducha','limpieza', 'ventilación','aire', 'sudor'],
            'STAFF/COACHES': ['profesor','entrenador', 'clase','atención', 'ayuda','rutina', 'coach','soberbio', 'instructor'],
            'OPERACIÓN': ['lleno','espera', 'música','horario', 'amontonado','cupo', 'inscripción','membresía']
        },
        "quejas": ['sucio', 'roto','malo', 'pésimo','lleno', 'caro','desorden', 'incómodo','pobre']
    }
}

def auditoria_estricta(texto, rubro):
    if not isinstance(texto, str) or str(texto).strip() == "": return 0
    texto_limpio = str(texto).lower()
    
    # Filtro de falsos positivos profesional
    palabras_positivas = ['rico', 'excelente','recomiendo', 'bueno','bien', 'espectacular','cómodo', 'limpio','amable']
    if any(p in texto_limpio for p in palabras_positivas):
        # Buscamos la primera coincidencia positiva
        pos_encontrada = [p for p in palabras_positivas if p in texto_limpio][0]
        # Si no hay un "no" antes de la palabra positiva, la damos por válida/buena
        if "no " not in texto_limpio.split(pos_encontrada)[0]:
            return 0
            
    sentimiento = TextBlob(str(texto)).sentiment.polarity
    palabras_queja = DICCIONARIOS.get(rubro, DICCIONARIOS["Gastronomía"])["quejas"]
    
    if any(p in texto_limpio for p in palabras_queja) or sentimiento < -0.1:
        return -1 
    return 0

def categorizar_falla(texto, rubro):
    texto = str(texto).lower()
    cats = DICCIONARIOS.get(rubro, DICCIONARIOS["Gastronomía"])["categorias"]
    for cat, palabras in cats.items():
        if any(p in texto for p in palabras): 
            return cat
    return "GENERAL"

def obtener_causa_raiz(df, col_resena):
    """
    Extrae las palabras más frecuentes de las quejas para identificar la raíz del problema.
    """
    texto_quejas = " ".join(df[col_resena].astype(str)).lower()
    palabras = re.findall(r'\b\w{5,}\b', texto_quejas)
    stop_words = ['estaba', 'fuimos','comida', 'porque','restaurante', 'lugar','cliente', 'gracias', 'excelente']
    frecuencia = Counter([p for p in palabras if p not in stop_words])
    return pd.DataFrame(frecuencia.most_common(10), columns=['Problema','Frecuencia'])

def procesar_auditoria(df, rubro='Gastronomía', col_resena='Reseña'):
    """
    Función puente para conectar con la lógica de app.py sin romper nada.
    """
    # Aplicamos tu auditoría estricta
    df['Resultado_Auditoria'] = df[col_resena].apply(lambda x: auditoria_estricta(x, rubro))
    # Categorizamos las fallas detectadas
    df['Fallas_Detectadas'] = df[col_resena].apply(lambda x: categorizar_falla(x, rubro) if auditoria_estricta(x, rubro) == -1 else "Sin fallas")
    return df
