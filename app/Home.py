import streamlit as st

st.set_page_config(
    page_title="Streaming Analytics | PI Minería de Datos I",
    page_icon="📺",
    layout="wide",
)

st.title("📺 Análisis de Usuarios de Plataforma de Streaming")
st.subheader("Proyecto Integrador — Minería de Datos I")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
### Contexto del proyecto

Este proyecto analiza el comportamiento de usuarios de una plataforma de streaming
de contenido latinoamericana. A partir de un dataset con **8.160 registros** y problemas
reales de calidad (valores imposibles, variantes de codificación, duplicados, outliers),
se desarrolló un pipeline completo de minería de datos que incluye:

- 🔍 **Inspección inicial** del dataset crudo
- 🧹 **Limpieza y preparación** con pipeline auditado (retención: 98.46%)
- 📊 **Análisis exploratorio** univariado, bivariado y multivariado
- 📉 **PCA** sobre variables numéricas, previo escalamiento obligatorio
- 💡 **Conclusiones** con hallazgos, limitaciones y próximos pasos

### Pregunta central
> ¿Qué factores distinguen el comportamiento de consumo de los usuarios de la plataforma?
""")

with col2:
    st.markdown("### Integrantes")
    st.markdown("👤 **Valeria Martinetti**")
    st.markdown("👤 **Santiago Gallardo**")
    st.divider()
    st.markdown("### Dataset")
    st.metric("Usuarios (original)", "8.160")
    st.metric("Usuarios (post-limpieza)", "8.034")
    st.metric("Retención", "98.46%")

st.divider()

st.markdown("""
### Navegación

Usá el menú lateral para explorar cada sección del análisis:

| Página | Contenido |
|---|---|
| 📁 **Dataset** | Descripción del dataset, calidad y transformaciones realizadas |
| 📊 **EDA** | Análisis exploratorio: distribuciones, correlaciones y patrones |
| 📉 **PCA** | Escalamiento, análisis de componentes principales e interpretación |
| 💡 **Conclusiones** | Hallazgos clave, limitaciones y próximos pasos |

### Repositorio
🔗 [Ver código fuente en GitHub](https://github.com/val-martinetti/PI_Mineria_Datos_1)
""")
