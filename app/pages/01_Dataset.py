import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path


st.set_page_config(page_title="Dataset | Streaming Analytics", page_icon="📁", layout="wide")

st.title("📁 Dataset — Descripción y Calidad")
st.caption("Fuente: `streaming_users_dirty.json` — dataset provisto por la cátedra")

@st.cache_data
def cargar_datos():
    BASE_DIR = Path(__file__).resolve().parents[2]
    raw_path = BASE_DIR / "data" / "raw" / "streaming_users_dirty.json" 
    clean_path = BASE_DIR / "data" / "processed" / "streaming_users_clean.csv"
    with open(raw_path) as f:
        df_raw = pd.DataFrame(json.load(f))
    df_clean = pd.read_csv(clean_path, parse_dates=["last_login_date"])
    return df_raw, df_clean

df_raw, df = cargar_datos()

st.header("1. Descripción del dataset")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
El dataset contiene registros de usuarios de una plataforma de streaming latinoamericana.
Cada fila representa un usuario con sus atributos demográficos, de comportamiento y de servicio al cliente.

| Variable | Tipo | Descripción |
|---|---|---|
| `user_id` | Numérica discreta | Identificador único |
| `age` | Numérica discreta | Edad en años |
| `subscription_plan` | Categórica nominal | Básico / Estándar / Premium |
| `monthly_watch_time_mins` | Numérica continua | Minutos vistos en el mes |
| `country` | Categórica nominal | País (7 países) |
| `favorite_genre` | Categórica nominal | Género favorito |
| `last_login_date` | Fecha | Último inicio de sesión |
| `customer_support_tickets` | Numérica discreta | Tickets de soporte |
""")
with col2:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("Métricas clave")
    ca, cb = st.columns(2)
    ca.metric("Registros (original)", f"{len(df_raw):,}")
    cb.metric("Registros (limpio)", f"{len(df):,}")
    ca.metric("Columnas", len(df_raw.columns))
    cb.metric("Retención pipeline", "98.46%")
    ca.metric("Países", df["country"].nunique())
    cb.metric("Géneros", df["favorite_genre"].nunique())

st.divider()
st.header("2. Problemas de calidad detectados y acciones")

problemas = pd.DataFrame({
    "Problema detectado": [
        "Duplicados exactos (sin user_id)",
        "Variantes en subscription_plan",
        "Variantes en country",
        "Variantes en favorite_genre",
        "age imposibles (< 1 o > 100 años)",
        "monthly_watch_time_mins nulos (originales)",
        "monthly_watch_time_mins imposibles (negativos o > 44.640, incl. centinela 99.999)",
        "monthly_watch_time_mins extremos reales (heavy users)",
        "customer_support_tickets imposibles (negativos o > 20, incl. centinela 150)",
        "customer_support_tickets extremos reales",
        "last_login_date nulas + inválidas",
        "favorite_genre nulos"
    ],
    "Cantidad": ["126", "15 → 3", "26 → 7", "28 → 7", "98", "193", "80", "108", "96", "14", "769", "1.340*"],
    "Acción tomada": [
        "Eliminados",
        "Mapeo explícito (normalización fonética)",
        "Mapeo ISO + inglés → español canónico",
        "Mapeo explícito + corrección tipográfica",
        "→ NaN; imputado con mediana global",
        "→ NaN; imputado con mediana global (junto con los 80 imposibles: 273 en total)",
        "→ NaN; imputado con mediana global",
        "Winsorizado k=3 (límite: 2.693,40 min/mes)",
        "→ NaN; imputado con mediana global (=1)",
        "Winsorizado k=3 (límite: 4 tickets)",
        "→ NaT (no imputables)",
        "Imputado con valor fijo 'Otros'"
    ]
})
st.dataframe(problemas, use_container_width=True, hide_index=True)
st.info("**Mecanismo MAR en watch_time:** la tasa de faltantes en Premium (10.4%) es x8 la de Básico (1.3%). La ausencia depende del plan → conviene imputar por mediana de cada plan en lugar de mediana global (pendiente de implementar; el pipeline actual usa mediana global).")
st.warning("""
**\\* Bug detectado en la normalización de `favorite_genre`:** el diccionario de mapeo usado en la
limpieza (`02_calidad_y_limpieza.ipynb`) nunca incluye la clave `'Crime': 'Crime'` (solo
`'Crimen': 'Crime'`, duplicada). Como resultado, los ~1.067 registros cuyo valor original ya era
`Crime` no matchean ninguna clave y `.map()` los convierte en nulos. Por eso los nulos de
`favorite_genre` pasan de 240 (inspección inicial) a 1.340 después de la normalización, y todos
esos casos terminan imputados con el valor fijo `'Otros'` — no con la moda. Esto infla
artificialmente la categoría `'Otros'` y deja a `Crime` con apenas ~40 registros reales. Conviene
corregir el diccionario y re-correr el pipeline antes de usar `favorite_genre` en cualquier
análisis.
""")

BASE_DIR = Path(__file__).resolve().parents[2]
st.divider()
st.header("3. Log del pipeline ETL")
log_path = BASE_DIR / "logs" / "pipeline_log.csv"
log_df = pd.read_csv(log_path)
st.dataframe(log_df, width="stretch", hide_index=True)
st.caption("Fuente: `logs/pipeline_log.csv`")

st.divider()
st.header("4. Vista previa del dataset limpio")
n = st.slider("Filas a mostrar:", 5, 50, 10)
st.dataframe(df.head(n), use_container_width=True)
st.subheader("Estadísticos descriptivos")
st.dataframe(df.describe().round(2), use_container_width=True)
