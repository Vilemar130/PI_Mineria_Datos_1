import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conclusiones | Streaming Analytics", page_icon="💡", layout="wide")
st.title("💡 Conclusiones del Análisis")

st.markdown("""
Este notebook consolida los hallazgos de todo el proceso de minería de datos,
diferenciando entre evidencia (lo que muestran los datos), interpretación
(lo que esos datos significan) y conclusión (la decisión o acción que habilitan).
""")

# ── HALLAZGOS ─────────────────────────────────────────────────────────────────
st.header("1. Hallazgos principales")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧹 Calidad y limpieza")
    st.success("""
**El dataset tenía problemas sistemáticos de ingesta, no errores aislados.**

- 15 variantes de subscription_plan, 26 de country, 28 de genre → sistema sin validación de esquema en origen
- Valores centinela (99.999, 99, 150) → campos que no admiten NULL en sistemas legacy
- Retención post-limpieza: **98.46%** (solo se perdió 1.54% por duplicados verificados)
- Mecanismo MAR detectado en watch_time: Premium tiene 8× más faltantes que Básico → posible bug de tracking
""")

    st.subheader("📊 EDA")
    st.info("""
**El plan de suscripción es el principal diferenciador del comportamiento de uso.**

- Básico: ~595 min/mes | Estándar: ~870 min/mes | **Premium: ~1.128 min/mes (+140% vs Básico)**
- La edad no predice el consumo: correlación edad–watch_time ≈ 0.00
- Distribución etaria simétrica (~33 años promedio, sin sesgo relevante)
- 7 países con distribución geográfica uniforme (~1.150 usuarios cada uno)
- 7 géneros con preferencias casi uniformes entre planes
""")

with col2:
    st.subheader("📉 PCA")
    st.warning("""
**Las 3 variables numéricas son ortogonales entre sí: no hay redundancia que comprimir.**

- StandardScaler obligatorio: watch_time (varianza ~10.000) dominaría sin escalamiento
- PC1 (~34%): dimensión de consumo (watch_time dominante)
- PC2 (~33%): dimensión demográfico-soporte (age + tickets)
- 2 componentes explican ~67% de la varianza
- La distribución uniforme de varianza entre PCs confirma la independencia entre variables
""")

    st.subheader("📍 Tabla evidencia → conclusión")
    tabla = pd.DataFrame({
        "Hallazgo": [
            "Retención 98.46%",
            "Premium: 10× más nulos en watch_time",
            "Premium: +140% watch_time",
            "Correlación edad–watch_time ≈ 0",
            "Varianza ~33% por PC",
        ],
        "Tipo": ["Evidencia", "Evidencia + Interpretación", "Evidencia + Conclusión", "Evidencia", "Evidencia + Interpretación"],
        "Acción sugerida": [
            "Validar proceso de limpieza",
            "Investigar bug de tracking en Premium",
            "Usar plan como segmentador principal",
            "No usar edad para predecir consumo",
            "Incorporar variables codificadas para PCA más potente"
        ]
    })
    st.dataframe(tabla, use_container_width=True, hide_index=True)

# ── LIMITACIONES ──────────────────────────────────────────────────────────────
st.divider()
st.header("2. Limitaciones del análisis")

lims = pd.DataFrame({
    "Limitación": [
        "769 fechas de login no utilizables (NaT)",
        "Categóricas excluidas del PCA",
        "Causalidad no establecida",
        "Sin datos históricos (snapshot único)",
        "Tickets winsorizados pierden magnitud extrema"
    ],
    "Implicancia": [
        "No se puede analizar retención, churn ni actividad reciente",
        "Plan, país y género —variables clave— no participan en el espacio dimensional",
        "Plan → watch_time es asociación, no causa probada",
        "No es posible analizar tendencias, estacionalidad ni cohortes",
        "Los casos extremos (99, 150) perdieron su valor real (posible sesgo al alza)"
    ],
    "Cómo superar": [
        "Corregir validación en el sistema origen; no imputar fechas",
        "Aplicar ordinal encoding (plan) o one-hot encoding (país/género) antes del PCA",
        "Diseñar A/B test: ofrecer upgrade a submuestra aleatoria de usuarios Básico",
        "Solicitar datos históricos para análisis de cohortes y series temporales",
        "Validar en el sistema origen si los valores eran reales o errores de carga"
    ]
})
st.dataframe(lims, use_container_width=True, hide_index=True)

# ── PRÓXIMOS PASOS ────────────────────────────────────────────────────────────
st.divider()
st.header("3. Próximos pasos")

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Con los datos actuales")
    st.markdown("""
1. **Codificar subscription_plan** como ordinal (Básico=1, Estándar=2, Premium=3) 
   e incorporarla al PCA para mayor separación entre grupos
2. **Calcular días_desde_last_login** para los ~7.200 registros con fecha válida 
   como proxy de actividad reciente
3. **Clustering K-Means** sobre el espacio PCA para segmentar automáticamente 
   perfiles de usuario
""")

with col4:
    st.markdown("#### Mejoras de fuente y modelo")
    st.markdown("""
4. **Validación de esquema en ingesta:** implementar rangos válidos, 
   valores permitidos para categóricas y formato de fecha estricto en el sistema origen
5. **Predicción de churn:** construir modelo supervisado usando plan, 
   watch_time y tickets como features
6. **Análisis de cohortes:** solicitar datos históricos para rastrear 
   la evolución del consumo por cohorte de registro
7. **Investigar nulos Premium:** la tasa de falta 8× mayor en Premium 
   sugiere un bug técnico de tracking que merece revisión en el sistema de logs
""")

st.divider()
st.markdown("""
---
> **Regla de cierre:** Calcular no es interpretar. El valor de este análisis no está en los
> gráficos ni en los números, sino en las preguntas que responden y las decisiones que habilitan.
> La brecha Premium–Básico (+140% en consumo) es el hallazgo más accionable: informa
> directamente la estrategia de conversión de usuarios Básico a planes superiores.
""")
