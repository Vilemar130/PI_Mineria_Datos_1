import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="EDA | Streaming Analytics", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos (EDA)")

@st.cache_data
def cargar_datos():
    base = os.path.dirname(os.path.dirname(__file__))
    return pd.read_csv(os.path.join(base, "data", "processed", "streaming_users_clean.csv"),
                       parse_dates=["last_login_date"])

df = cargar_datos()
sns.set_theme(style="whitegrid", palette="muted")

st.markdown("""
### Preguntas que guían el EDA
1. ¿Cuál es el perfil típico del usuario de la plataforma?
2. ¿El tiempo de visualización varía según el plan de suscripción?
3. ¿Existe relación entre edad y consumo?
4. ¿Cómo se distribuyen géneros y países?
5. ¿El soporte técnico varía según el plan?
""")

# ── ANÁLISIS UNIVARIADO ────────────────────────────────────────────────────────
st.divider()
st.header("1. Análisis Univariado")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de edad")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(df["age"], bins=30, color="steelblue", edgecolor="white", alpha=0.85)
    ax.axvline(df["age"].mean(), color="red", linestyle="--", lw=1.5, label=f"Media: {df['age'].mean():.1f}")
    ax.axvline(df["age"].median(), color="orange", linestyle="--", lw=1.5, label=f"Mediana: {df['age'].median():.1f}")
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Frecuencia")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption(f"Media: {df['age'].mean():.1f} | Mediana: {df['age'].median():.1f} | Desvío: {df['age'].std():.1f} | Asimetría: {df['age'].skew():.2f}")
    st.markdown("**Interpretación:** distribución aproximadamente simétrica (skew ≈ 0.14). El 50% central de usuarios tiene entre 25 y 42 años. La edad promedio es ~33 años.")

with col2:
    st.subheader("Distribución de planes")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    counts = df["subscription_plan"].value_counts().reindex(["Básico", "Estándar", "Premium"])
    bars = ax.bar(counts.index, counts.values, color=["#4e79a7", "#f28e2b", "#59a14f"], alpha=0.85)
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=9)
    ax.set_ylabel("Usuarios")
    ax.set_ylim(0, counts.max() * 1.15)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption(f"Básico: {counts['Básico']:,} (44.9%) | Estándar: {counts['Estándar']:,} (35.3%) | Premium: {counts['Premium']:,} (19.8%)")
    st.markdown("**Interpretación:** casi la mitad de la base elige el plan más económico (Básico). Premium concentra solo el 20% de los usuarios.")

# ── ANÁLISIS BIVARIADO ────────────────────────────────────────────────────────
st.divider()
st.header("2. Análisis Bivariado")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Watch time por plan de suscripción")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    orden = ["Básico", "Estándar", "Premium"]
    medias = df.groupby("subscription_plan")["monthly_watch_time_mins"].mean().reindex(orden)
    medianas = df.groupby("subscription_plan")["monthly_watch_time_mins"].median().reindex(orden)
    x = range(len(orden))
    bars = ax.bar(x, medias.values, color=["#4e79a7", "#f28e2b", "#59a14f"], alpha=0.85)
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(orden)
    ax.set_ylabel("Minutos/mes (media)")
    ax.set_ylim(0, medias.max() * 1.2)
    plt.tight_layout()
    st.pyplot(fig)
    for plan in orden:
        g = df[df["subscription_plan"] == plan]["monthly_watch_time_mins"]
        st.caption(f"{plan}: media={g.mean():.0f} min | mediana={g.median():.0f} min")
    st.markdown("**Interpretación:** los usuarios Premium visualizan ~2.4× más contenido que los Básico (+140%). El plan es el principal diferenciador de consumo.")

with col4:
    st.subheader("Edad vs. Tiempo de visualización")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    muestra = df.sample(min(2000, len(df)), random_state=42)
    ax.scatter(muestra["age"], muestra["monthly_watch_time_mins"], alpha=0.15, s=8, color="steelblue")
    z = np.polyfit(df["age"].dropna(), df.loc[df["age"].notna(), "monthly_watch_time_mins"], 1)
    p = np.poly1d(z)
    x_l = np.linspace(df["age"].min(), df["age"].max(), 100)
    corr = df[["age", "monthly_watch_time_mins"]].corr().iloc[0, 1]
    ax.plot(x_l, p(x_l), "r--", lw=2, label=f"r = {corr:.3f}")
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("Minutos/mes")
    ax.legend(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption(f"Correlación de Pearson: {corr:.4f}")
    st.markdown("**Interpretación:** correlación prácticamente nula. La edad **no predice** el consumo: usuarios de todas las edades tienen comportamientos similares.")

# ── ANÁLISIS MULTIVARIADO ─────────────────────────────────────────────────────
st.divider()
st.header("3. Análisis Multivariado")
st.subheader("Edad × Watch time × Plan de suscripción")

palette_plan = {"Básico": "#4e79a7", "Estándar": "#f28e2b", "Premium": "#59a14f"}
fig, ax = plt.subplots(figsize=(10, 4.5))
muestra = df.sample(min(2000, len(df)), random_state=1)
for plan, grupo in muestra.groupby("subscription_plan"):
    ax.scatter(grupo["age"], grupo["monthly_watch_time_mins"],
               label=plan, color=palette_plan[plan], alpha=0.35, s=15)
ax.set_xlabel("Edad (años)")
ax.set_ylabel("Minutos visualizados/mes")
ax.set_title("Edad vs. Watch time según plan de suscripción")
ax.legend(title="Plan")
plt.tight_layout()
st.pyplot(fig)
st.markdown("""
**Interpretación:** las tres nubes se superponen horizontalmente (la edad no diferencia planes), 
pero se **separan verticalmente** (Premium arriba, Básico abajo). Esto confirma que el plan es 
el principal factor diferenciador del consumo, independientemente de la edad del usuario.
""")

# ── HEATMAP ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Heatmap de correlaciones entre variables numéricas")
numeric_cols = ["age", "monthly_watch_time_mins", "customer_support_tickets"]
corr_matrix = df[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(5, 3.5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, fmt=".3f", square=True, ax=ax, linewidths=0.5)
ax.set_title("Correlaciones numéricas")
plt.tight_layout()
st.pyplot(fig)
st.markdown("**Interpretación:** correlaciones cercanas a 0 entre todas las variables numéricas. Las tres capturan dimensiones de variación independientes entre sí (sin redundancia).")

# ── DISTRIBUCIÓN GEOGRÁFICA ───────────────────────────────────────────────────
st.divider()
st.subheader("Distribución geográfica de usuarios")
fig, ax = plt.subplots(figsize=(8, 3.5))
paises = df["country"].value_counts().sort_values()
ax.barh(paises.index, paises.values, color="steelblue", alpha=0.8)
ax.bar_label(ax.containers[0], fmt="%d", padding=3, fontsize=9)
ax.set_xlabel("Usuarios")
ax.set_xlim(0, paises.max() * 1.12)
plt.tight_layout()
st.pyplot(fig)
st.markdown("**Interpretación:** distribución casi uniforme entre los 7 países (~1.150 usuarios cada uno). No hay un mercado dominante: la plataforma tiene presencia regional equilibrada.")
