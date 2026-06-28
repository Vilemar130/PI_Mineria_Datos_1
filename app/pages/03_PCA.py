import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
from pathlib import Path

st.set_page_config(page_title="PCA | Streaming Analytics", page_icon="📉", layout="wide")
st.title("📉 Escalamiento y Análisis de Componentes Principales (PCA)")

@st.cache_data
def cargar_y_computar():
    BASE_DIR = Path(__file__).resolve().parents[2]
    df = pd.read_csv(BASE_DIR / "data" / "processed" / "streaming_users_clean.csv")
    features = ["age", "monthly_watch_time_mins", "customer_support_tickets"]
    X = df[features].copy()

    # Escalamiento
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=features, index=X.index)

    # PCA completo
    pca_full = PCA(n_components=3, random_state=42)
    pca_full.fit(X_scaled)

    # PCA 2 componentes
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"], index=df.index)

    loadings = pd.DataFrame(pca.components_, columns=features, index=["PC1", "PC2"])
    return df, X, X_scaled, pca_full, pca, X_pca_df, loadings

df, X, X_scaled, pca_full, pca, X_pca_df, loadings = cargar_y_computar()
sns.set_theme(style="whitegrid")

# ── VARIABLES ─────────────────────────────────────────────────────────────────
st.header("1. Variables seleccionadas")
vars_df = pd.DataFrame({
    "Variable": ["age", "monthly_watch_time_mins", "customer_support_tickets"],
    "Descripción": ["Edad del usuario", "Minutos de contenido visto al mes", "Tickets de soporte generados"],
    "Justificación": [
        "Perfil demográfico",
        "Intensidad de consumo de contenido",
        "Interacción con el servicio técnico"
    ]
})
st.dataframe(vars_df, use_container_width=True, hide_index=True)
st.caption("Variables excluidas: user_id (identificador), categóricas (requieren codificación), last_login_date (769 NaT)")

# ── POR QUÉ ESCALAR ───────────────────────────────────────────────────────────
st.divider()
st.header("2. ¿Por qué es obligatorio escalar antes del PCA?")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Varianzas sin escalar")
    var_df = X.var().round(2).reset_index()
    var_df.columns = ["Variable", "Varianza"]
    st.dataframe(var_df, use_container_width=True, hide_index=True)
    st.error("Sin escalar, `monthly_watch_time_mins` domina el PCA por su magnitud, no por relevancia analítica.")
with col2:
    st.subheader("Varianzas post-escalado (StandardScaler)")
    var_sc = X_scaled.var().round(4).reset_index()
    var_sc.columns = ["Variable", "Varianza"]
    st.dataframe(var_sc, use_container_width=True, hide_index=True)
    st.success("Tras estandarizar, todas las variables tienen varianza = 1 y contribuyen de forma equitativa.")

st.markdown("""
**Técnica usada:** `StandardScaler` (Z-score) → $x' = \\frac{x - \\mu}{\\sigma}$

Se eligió Z-score (en lugar de Min-Max) porque PCA preserva la distribución relativa de los datos,
y los outliers moderados (heavy users) son parte del patrón real del dataset.
""")

# ── VARIANZA EXPLICADA ────────────────────────────────────────────────────────
st.divider()
st.header("3. Varianza explicada por componente")

var_expl = pca_full.explained_variance_ratio_
var_acum = np.cumsum(var_expl)

col3, col4 = st.columns(2)
with col3:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(["PC1", "PC2", "PC3"], var_expl * 100, color=["#4e79a7", "#f28e2b", "#59a14f"], alpha=0.85)
    ax.plot(["PC1", "PC2", "PC3"], var_expl * 100, "ko-", markersize=6)
    ax.set_ylabel("Varianza explicada (%)")
    ax.set_title("Scree Plot")
    for i, v in enumerate(var_expl * 100):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(["PC1", "PC2", "PC3"], var_acum * 100, "bo-", markersize=8)
    ax.axhline(y=80, color="red", linestyle="--", alpha=0.7, label="Umbral 80%")
    ax.set_ylabel("Varianza acumulada (%)")
    ax.set_title("Varianza acumulada")
    ax.legend()
    for i, v in enumerate(var_acum * 100):
        ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

var_tab = pd.DataFrame({
    "Componente": ["PC1", "PC2", "PC3"],
    "Varianza explicada (%)": [f"{v*100:.1f}%" for v in var_expl],
    "Varianza acumulada (%)": [f"{v*100:.1f}%" for v in var_acum]
})
st.dataframe(var_tab, use_container_width=True, hide_index=True)

st.info("""
**Interpretación del Scree Plot:** las tres componentes explican partes casi iguales de la varianza (~33% cada una).
Esto ocurre porque las variables de entrada tienen correlaciones ≈ 0 entre sí (verificado en el EDA):
cuando las variables son independientes, PCA no puede comprimir — cada variable ya es, por sí sola, una componente.

**Decisión:** se retienen **2 componentes** (67% de varianza) para habilitar visualización 2D.
""")

# ── CARGAS (LOADINGS) ─────────────────────────────────────────────────────────
st.divider()
st.header("4. Cargas (loadings) de las variables")

col5, col6 = st.columns(2)
with col5:
    st.dataframe(loadings.round(4), use_container_width=True)
    st.markdown("""
**Interpretación:**
- **PC1:** dominada por `monthly_watch_time_mins` → "dimensión de consumo"
  - Puntuación alta = heavy user
- **PC2:** combinación de `age` + `customer_support_tickets` → "dimensión demográfico-soporte"
  - Puntuación alta = usuario mayor con más demanda de soporte técnico
""")

with col6:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    loadings.T.plot(kind="bar", ax=ax, colormap="Set2", alpha=0.85, edgecolor="white")
    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.set_ylabel("Carga (loading)")
    ax.set_title("Cargas de variables en PC1 y PC2")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(title="Componente")
    plt.tight_layout()
    st.pyplot(fig)

# ── SCATTER PCA ───────────────────────────────────────────────────────────────
st.divider()
st.header("5. Visualización en espacio PCA")

df_pca = X_pca_df.join(df[["subscription_plan", "age", "monthly_watch_time_mins"]])
palette_plan = {"Básico": "#4e79a7", "Estándar": "#f28e2b", "Premium": "#59a14f"}

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
for plan, grupo in df_pca.groupby("subscription_plan"):
    axes[0].scatter(grupo["PC1"], grupo["PC2"], label=plan, color=palette_plan[plan], alpha=0.25, s=8)
axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varianza)")
axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varianza)")
axes[0].set_title("Espacio PCA — por plan")
axes[0].legend(title="Plan", markerscale=3)

sc = axes[1].scatter(df_pca["PC1"], df_pca["PC2"], c=df_pca["age"], cmap="viridis", alpha=0.25, s=8)
plt.colorbar(sc, ax=axes[1], label="Edad (años)")
axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% varianza)")
axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% varianza)")
axes[1].set_title("Espacio PCA — por edad")

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
**Interpretación:**
- **Por plan:** los usuarios Premium se desplazan hacia la derecha en PC1 (mayor consumo), coherente con el EDA.
- **Por edad:** el gradiente vertical en PC2 refleja que la edad sí diferencia el eje PC2 (dimensión demográfica), 
  aunque con dispersión alta — el plan sigue siendo más discriminante.
""")
