import pandas as pd
import streamlit as st

st.set_page_config(page_title="Conclusiones | Proyecto Integrador", page_icon="✅", layout="wide")

st.title("✅ Conclusiones")
st.caption("Síntesis de hallazgos, limitaciones y próximos pasos del proyecto.")

# ── Hallazgos ────────────────────────────────────────────────────────────
st.header("Hallazgos")

with st.expander("Inspección y calidad del dataset", expanded=True):
    st.markdown(
        """
**Evidencia:** dataset original de 8.160 registros × 8 columnas, con 126 duplicados
exactos, 15 variantes de texto en `subscription_plan`, 26 en `country` y 28 en
`favorite_genre`; 120 valores imposibles en `age`, 49 negativos en `monthly_watch_time_mins`,
29 negativos en `customer_support_tickets`, y 769 fechas no utilizables en `last_login_date`.

**Interpretación:** los problemas de codificación en las categóricas (mayúsculas, tildes,
abreviaturas, mezcla de idiomas) sugieren datos provenientes de múltiples sistemas de
ingesta sin un esquema de validación unificado. Los valores como 99, 150 y 99 999 son
"valores centinela" típicos de errores de carga en sistemas legacy. El mecanismo de
falta en `monthly_watch_time_mins` es **MAR**: la tasa de nulos en Premium (10.4%) es
8 veces la de Básico (1.3%), lo que sugiere que la pérdida de datos está asociada al plan.

**Conclusión:** el dataset tenía problemas de calidad sistemáticos y heterogéneos. El
pipeline de limpieza los resolvió con criterio de dominio documentado, alcanzando
**98.46% de retención estructural** (solo se perdió 1.54% por duplicados verificados).
"""
    )

with st.expander("Análisis exploratorio (EDA)", expanded=True):
    st.markdown(
        """
**Evidencia:** el plan Premium presenta el mayor consumo promedio, muy por encima de
Estándar y Básico. La correlación entre edad y tiempo de visualización es prácticamente
nula. Las tres variables numéricas (`age`, `monthly_watch_time_mins`,
`customer_support_tickets`) están, entre sí, muy poco correlacionadas.

**Interpretación:** la brecha de consumo entre Premium y Básico no puede explicarse solo
por diferencia de acceso a contenido — es posible que los heavy users elijan Premium, o
que el mayor acceso genere mayor consumo (asociación, no causalidad). La independencia
de la edad respecto al consumo es un hallazgo contraintuitivo: la plataforma parece
atraer y retener usuarios de todas las edades con patrones de uso similares.

**Conclusión:** el **plan de suscripción** es el principal diferenciador del comportamiento
de uso de la plataforma. La edad, el género favorito y el país no predicen por sí solos
el nivel de consumo.
"""
    )

with st.expander("PCA", expanded=True):
    st.markdown(
        """
**Evidencia:** con `age`, `monthly_watch_time_mins` y `customer_support_tickets`
estandarizados (StandardScaler), las tres componentes principales explican una
proporción de varianza casi pareja entre sí; 2 componentes alcanzan aproximadamente
67% de varianza acumulada.

**Interpretación:** la distribución casi uniforme de varianza entre componentes es
consecuencia directa de la baja correlación entre las variables de entrada (verificada
en el EDA). Cuando las variables son ortogonales, el PCA no puede comprimir de forma
eficiente: cada componente termina heredando, en gran medida, una sola variable.

**Conclusión:** el PCA confirma que las variables cuantitativas disponibles capturan
dimensiones de variación independientes entre sí — no hay redundancia que comprimir.
Para un PCA más informativo sería necesario incorporar variables adicionales o
transformadas (p. ej. plan codificado, días desde el último login).
"""
    )

# ── Limitaciones ─────────────────────────────────────────────────────────
st.header("Limitaciones")

st.markdown(
    """
1. **Mecanismo no resuelto en fechas:** cientos de fechas de último login quedaron como
   `NaT` (nulas o inválidas). Sin ellas no es posible analizar actividad reciente ni
   calcular métricas de retención o *churn*.
2. **Variables categóricas excluidas del PCA:** `subscription_plan`, `country` y
   `favorite_genre` son muy relevantes para el negocio pero no se incorporaron al PCA
   por ser nominales. Además, `subscription_plan` y `country` conservan nulos residuales
   por variantes de texto no cubiertas por el mapeo de normalización, lo que reduce el
   tamaño de muestra disponible para los análisis que las involucran.
3. **Causalidad no establecida:** la relación entre plan y tiempo de visualización es una
   asociación observada, no una relación causal comprobada.
4. **Ausencia de datos históricos:** el dataset es una foto (*snapshot*) puntual; sin
   series temporales no es posible analizar tendencias de crecimiento, *churn* o
   estacionalidad.
5. **Winsorización de tickets de soporte:** se acotaron a un máximo definido por IQR
   (k=3). Los casos extremos originales (99, 150) perdieron su magnitud real, aunque el
   análisis los identificó como probables errores de carga y no consumo genuino.
"""
)

# ── Próximos pasos ────────────────────────────────────────────────────────
st.header("Próximos pasos")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
**Inmediato (con los datos actuales)**
- Codificar `subscription_plan` de forma ordinal e incorporarla al PCA.
- Calcular días desde el último login como proxy de actividad reciente (para los
  registros con fecha válida).
- Revisar y, de ser posible, recuperar las variantes de texto de `subscription_plan` /
  `country` que quedaron sin mapear, para reducir la pérdida de información.

**Mejoras en la fuente de datos**
- Implementar validación de esquema en la ingesta (rangos válidos, catálogo cerrado
  de categóricas, formato de fecha estricto).
- Unificar la codificación de categóricas en el sistema de origen (usar IDs en lugar
  de texto libre).
"""
    )
with col2:
    st.markdown(
        """
**Modelado futuro**
- *Clustering* (K-Means) sobre los *scores* del PCA para segmentar usuarios.
- Modelo de predicción de *churn* usando plan, tiempo de visualización y tickets como
  variables predictoras.
- Análisis de cohortes si se logran obtener datos históricos.

**Comunicación**
- Compartir con el equipo de producto la brecha de consumo Premium–Básico como insumo
  directo para decisiones de *pricing*.
- Investigar cualitativamente por qué `monthly_watch_time_mins` tiene mayor tasa de
  nulos en el plan Premium (posible problema técnico de *tracking*).
"""
    )

# ── Tabla resumen ──────────────────────────────────────────────────────
st.header("Tabla resumen: evidencia → interpretación → conclusión")

resumen = pd.DataFrame({
    "Hallazgo": [
        "Pipeline con retención 98.46%",
        "Premium: mucho mayor tasa de faltantes en watch_time",
        "Premium consume notablemente más que Básico",
        "Correlación edad–watch_time ≈ 0",
        "PCA: varianza repartida casi por igual entre componentes",
    ],
    "Tipo": [
        "Evidencia",
        "Evidencia + Interpretación (MAR)",
        "Evidencia + Conclusión",
        "Evidencia",
        "Evidencia + Interpretación",
    ],
    "Implicancia": [
        "Calidad del proceso de limpieza",
        "Posible problema de tracking en cuentas Premium",
        "El plan es el principal segmentador de uso",
        "La edad no es un buen predictor de consumo",
        "Las variables numéricas son prácticamente independientes entre sí",
    ],
})
st.dataframe(resumen, use_container_width=True, hide_index=True)
