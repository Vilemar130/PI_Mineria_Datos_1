import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="EDA | Proyecto Integrador", page_icon="📊", layout="wide")

st.title("📊 Análisis Exploratorio de Datos (EDA)")
st.caption(
    "5 visualizaciones — 2 univariadas, 2 bivariadas y 1 multivariada — organizadas "
    "según las preguntas de análisis del proyecto."
)

@st.cache_data
def cargar_datos():
    BASE_DIR = Path(__file__).resolve().parents[2]
    clean_path = BASE_DIR / "data" / "processed" / "streaming_users_clean.csv"
    return pd.read_csv(clean_path, parse_dates=["last_login_date"])

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("No se encontró el archivo de datos procesados. Revisa la ruta.")
    st.stop()

ORDEN_PLAN = ['Básico', 'Estándar', 'Premium']
PALETTE = {"Básico": "#4e79a7", "Estándar": "#f28e2b", "Premium": "#59a14f"}

# ═══════════════════════════════════════════════════════════════════════
st.header("1. Análisis univariado")

# ── Pregunta 4: Distribución del tiempo de visualización ────────────────
st.subheader("Pregunta 1 — ¿Como se distribuye el tiempo de visualización mensual de los usuarios?")

s = df["monthly_watch_time_mins"]
fig1 = px.histogram(
    df, x="monthly_watch_time_mins", nbins=40,
    color_discrete_sequence=["teal"],
    labels={"monthly_watch_time_mins": "Minutos / mes"},
)
fig1.add_vline(x=s.mean(), line_dash="dash", line_color="red",
                annotation_text=f"Media: {s.mean():.0f}")
fig1.add_vline(x=s.median(), line_dash="dash", line_color="orange",
                annotation_text=f"Mediana: {s.median():.0f}")
fig1.update_layout(title="Tiempo de visualización mensual — Histograma", height=450)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
**Interpretación:** El tiempo de visualización mensual tiene asimetría positiva moderada, con media≈783 min por encima de la mediana ≈759 min, hay una cola de usuarios con alto consumo. El 50% central se ubica entre ≈500 y ≈1.029 minutos/mes, 8 a 17 horas. El máximo quedó acotado en ≈2.693 min por la winsorización aplicada en la limpieza, que eliminó el valor centinela 99.999 sin destruir el patrón real de los usuarios de mayor consumo. Esta distribución es la base sobre la que se apoya la pregunta sobre la relación entre tiempo de visualización y plan de suscripción.
"""
)

# ── Pregunta 5: Distribución de la edad ────────────────────────────────────
st.subheader("Pregunta 2 — ¿Como se distribuye la edad de los usuarios?")

a = df["age"]
fig2 = px.histogram(
    df, x="age", nbins=20,
    color_discrete_sequence=["steelblue"],
    labels={"age": "Edad (años)"},
)
fig2.add_vline(x=a.mean(), line_dash="dash", line_color="red",
                annotation_text=f"Media: {a.mean():.0f}")
fig2.add_vline(x=a.median(), line_dash="dash", line_color="orange",
                annotation_text=f"Mediana: {a.median():.0f}")
fig2.update_layout(title="Distribución de la Edad", height=450)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
**Interpretación:** La edad promedio de usuarios es 33 años. El Histograma nos muestra una distribución amplia que cubre desde jóvenes hasta adultos mayores, reflejando una base de usuarios variada.
"""
)

# ═══════════════════════════════════════════════════════════════════════
st.header("2. Análisis bivariado")

# ── Pregunta 1: Tiempo de visualización vs plan ────────────────────────
st.subheader("Pregunta 3 — ¿Como se distribuye el tiempo de visualización mensual según el plan de suscripción?")

fig3 = px.box(
    df, x="subscription_plan", y="monthly_watch_time_mins",
    category_orders={"subscription_plan": ORDEN_PLAN}, color="subscription_plan",
    color_discrete_map=PALETTE,
    labels={"subscription_plan": "Plan de suscripción", "monthly_watch_time_mins": "Minutos/mes"},
)
fig3.update_layout(title="Tiempo promedio de visualización por plan — Boxplot", showlegend=False, height=450)
st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    """
**Interpretación:** El plan de suscripción es un diferenciador claro del consumo. Los usuarios Premium visualizan en promedio 1.085 min/mes, los Estándar 860 min/mes y los Básico 589 min/mes. Hay una brecha Premium–Básico, y las cajas del boxplot casi no se superponen, lo que indica una separación consistente y no solo un efecto de outliers. El patrón es coherente con la idea de que el plan más caro atrae o genera usuarios de mayor consumo.
"""
)

# ── Pregunta 2: Edad vs Minutos de visualización ────────────────────────
st.subheader("Pregunta 4 — ¿Existe relación entre edad y minutos de visualización?")

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=df['age'], y=df['monthly_watch_time_mins'],
    mode='markers',
    marker=dict(color='steelblue', size=5, opacity=0.3),
    name='Usuarios'
))
z = np.polyfit(df['age'], df['monthly_watch_time_mins'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['age'].min(), df['age'].max(), 100)
fig4.add_trace(go.Scatter(
    x=x_line, y=p(x_line),
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name=f'Tendencia (pendiente: {z[0]:.2f} min/año)'
))
corr = df[['age', 'monthly_watch_time_mins']].corr().iloc[0, 1]
fig4.update_layout(
    title=f"Edad vs. Tiempo de visualización (r = {corr:.4f})",
    xaxis_title="Edad (años)",
    yaxis_title="Minutos visualizados/mes",
    height=450
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    """
**Interpretación:** La correlación entre edad y tiempo de visualización es prácticamente nula y la línea de tendencia es casi horizontal. La edad no predice el consumo de contenido: usuarios jóvenes y mayores presentan niveles de visualización similares. Esto refuerza el hallazgo de la Visualización 3, el plan de suscripción explica el consumo, no la edad del usuario.
"""
)

# ═══════════════════════════════════════════════════════════════════════
st.header("3. Análisis multivariado")

# ── Pregunta 3: Tickets vs plan vs país ─────────────────────────────────
st.subheader("Pregunta 5 — ¿Existen diferencias en la cantidad promedio de tickets de soporte entre los distintos países y planes de suscripción?")

df_geo = df.dropna(subset=['country', 'subscription_plan'])
pivot = df_geo.pivot_table(
    index="subscription_plan", columns="country", values="customer_support_tickets",
    aggfunc="mean", observed=True,
).reindex(ORDEN_PLAN)

fig5 = px.imshow(
    pivot.round(2), text_auto=True, color_continuous_scale="OrRd", aspect="auto",
    labels=dict(x="País", y="Plan", color="Tickets promedio"),
)
fig5.update_layout(title="Tickets de soporte promedio por país y plan", height=420)
st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    """
**Interpretación:** Se puede observar que los tickets de soporte no están asociados de forma relevante ni al plan ni al país. Estas actúan como variables independientes de los tickets de soporte. El heatmap compara el promedio de tickets por país y plan, permitiendo identificar que las diferencias entre las distintas combinaciones son mínimas y no hay un patrón dominante.
"""
)

st.divider()
st.caption(
    "Todas las visualizaciones usan el dataset ya limpio (post-pipeline). Las variables "
    "`subscription_plan` y `country` conservan nulos residuales — ver página Dataset — "
    "por lo que los cálculos que las involucran se hacen sobre el subconjunto con valor válido."
)
