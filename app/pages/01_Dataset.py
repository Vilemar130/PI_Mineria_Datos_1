import streamlit as st
import pandas as pd
import numpy as np
import os
import json

st.set_page_config(page_title="Dataset | Streaming Analytics", page_icon="📁", layout="wide")

st.title("📁 Dataset — Descripción y Calidad")
st.caption("Fuente: `streaming_users_dirty.json` — dataset provisto por la cátedra")

@st.cache_data
def cargar_datos():
    base = os.path.dirname(os.path.dirname(__file__))
    raw_path = os.path.join(base, "data", "raw", "streaming_users_dirty.json")
    clean_path = os.path.join(base, "data", "processed", "streaming_users_clean.csv")
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
        "age imposibles (< 6 o > 100 años)",
        "monthly_watch_time_mins negativos",
        "monthly_watch_time_mins nulos (originales)",
        "monthly_watch_time_mins extremos (valor centinela 99.999)",
        "customer_support_tickets negativos",
        "customer_support_tickets extremos (99, 150)",
        "last_login_date nulas + inválidas",
        "favorite_genre nulos"
    ],
    "Cantidad": ["126", "15 → 3", "26 → 7", "28 → 7", "120", "49", "193", "139", "29", "81", "769", "240"],
    "Acción tomada": [
        "Eliminados",
        "Mapeo explícito (normalización fonética)",
        "Mapeo ISO + inglés → español canónico",
        "Mapeo explícito + corrección tipográfica",
        "→ NaN; imputado con mediana global (MCAR)",
        "→ NaN; imputado con mediana por plan",
        "Imputado con mediana por plan (MAR)",
        "Winsorizado k=3 (límite: 2.705 min/mes)",
        "→ NaN; imputado con mediana global",
        "Winsorizado k=3 (límite: 4 tickets)",
        "→ NaT (no imputables)",
        "Imputado con moda global (Comedia)"
    ]
})
st.dataframe(problemas, use_container_width=True, hide_index=True)
st.info("**Mecanismo MAR en watch_time:** la tasa de faltantes en Premium (10.4%) es 8× la de Básico (1.3%). La ausencia depende del plan → imputación por mediana de cada plan, no mediana global.")

st.divider()
st.header("3. Log del pipeline ETL")
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "pipeline_log.csv")
log_df = pd.read_csv(log_path)
st.dataframe(log_df, use_container_width=True, hide_index=True)
st.caption("Fuente: `logs/pipeline_log.csv`")

st.divider()
st.header("4. Vista previa del dataset limpio")
n = st.slider("Filas a mostrar:", 5, 50, 10)
st.dataframe(df.head(n), use_container_width=True)
st.subheader("Estadísticos descriptivos")
st.dataframe(df.describe(include="all").round(2), use_container_width=True)
