# PI_Mineria_Datos_1

Proyecto Integrador — Minería de Datos I

---

## 1. Integrantes y comisión

- **Val Martinetti** — val.martinetti@gmail.com

---

## 2. Descripción del proyecto

Análisis de datos reproducible sobre un dataset de usuarios de una plataforma de streaming latinoamericana (`streaming_users_dirty.json`, 8.160 registros × 8 columnas). El proyecto cubre el ciclo completo: inspección → calidad → EDA → PCA → conclusiones, implementado en notebooks Jupyter y comunicado en una app Streamlit pública.

**Pregunta central:** ¿Qué factores distinguen el comportamiento de consumo de los usuarios de la plataforma?

---

## 3. Dataset

- **Fuente:** `data/raw/streaming_users_dirty.json` — dataset provisto por la cátedra (inmutable)
- **Dataset procesado:** `data/processed/streaming_users_clean.csv`
- **Variables:** user_id, age, subscription_plan, monthly_watch_time_mins, country, favorite_genre, last_login_date, customer_support_tickets
- **Países:** Argentina, Brasil, Chile, Colombia, México, Perú, Uruguay
- **Planes:** Básico, Estándar, Premium

---

## 4. Estructura del repositorio

```
PI_Mineria_Datos_1/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/            ← dataset original SIN modificar
│   └── processed/      ← dataset limpio generado por el pipeline
├── notebooks/
│   ├── 01_inspeccion_inicial.ipynb
│   ├── 02_calidad_y_limpieza.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_pca.ipynb
│   └── 05_conclusiones.ipynb
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 01_Dataset.py
│       ├── 02_EDA.py
│       ├── 03_PCA.py
│       └── 04_Conclusiones.py
├── reports/
│   └── informe_final.pdf
└── logs/
    └── pipeline_log.csv
```

---

## 5. Pipeline de limpieza (resumen)

| Paso | Acción | Retención |
|---|---|---|
| 0 | Dataset original | 100.00% |
| 1 | Eliminación de 126 duplicados | 98.46% |
| 2–4 | Normalización categóricas (plan/país/género) | 98.46% |
| 5 | Valores imposibles en age → NaN | 98.46% |
| 6–7 | Negativos en tickets y watch_time → NaN | 98.46% |
| 8–9 | Winsorización outliers extremos (k=3) | 98.46% |
| 10 | Parseo fechas (inválidas → NaT) | 98.46% |
| 11 | Imputación diferenciada por mecanismo | 98.46% |

Log completo: [`logs/pipeline_log.csv`](logs/pipeline_log.csv)

---

## 6. Notebooks

| Notebook | Contenido |
|---|---|
| [`01_inspeccion_inicial.ipynb`](notebooks/01_inspeccion_inicial.ipynb) | Estructura, estadísticos, faltantes, duplicados, problemas |
| [`02_calidad_y_limpieza.ipynb`](notebooks/02_calidad_y_limpieza.ipynb) | Pipeline auditado de limpieza con justificación de cada decisión |
| [`03_eda.ipynb`](notebooks/03_eda.ipynb) | Análisis univariado, bivariado y multivariado |
| [`04_pca.ipynb`](notebooks/04_pca.ipynb) | Escalamiento, PCA, varianza explicada, interpretación de componentes |
| [`05_conclusiones.ipynb`](notebooks/05_conclusiones.ipynb) | Hallazgos, limitaciones y próximos pasos |

---

## 7. Hallazgos principales

1. **El plan de suscripción es el principal diferenciador:** Premium consume +140% más contenido que Básico (~1.300 vs ~540 min/mes)
2. **La edad no predice el consumo:** correlación edad–watch_time ≈ 0.00
3. **Mecanismo MAR detectado:** la tasa de faltantes en watch_time es 8× mayor en Premium que en Básico → posible bug de tracking
4. **Variables numéricas independientes:** correlaciones < 0.05 entre sí — sin redundancia en el dataset

---

## 8. App Streamlit

La app presenta los resultados del análisis de forma interactiva:

- 🔗 **App pública:** [Agregar URL luego del deploy en Streamlit Cloud]
- `Home.py` — Portada y contexto
- `01_Dataset.py` — Descripción, calidad y log ETL
- `02_EDA.py` — Análisis exploratorio (5 visualizaciones)
- `03_PCA.py` — Escalamiento y PCA
- `04_Conclusiones.py` — Hallazgos y próximos pasos

Para ejecutar localmente:
```bash
pip install -r requirements.txt
streamlit run app/Home.py
```

---

## 9. Informe final

Ver: [`reports/informe_final.pdf`](reports/informe_final.pdf)

---

## 10. Instrucciones de reproducibilidad

```bash
# 1. Clonar el repositorio
git clone https://github.com/val-martinetti/PI_Mineria_Datos_1.git
cd PI_Mineria_Datos_1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar los notebooks en orden (1 → 5) con Jupyter
jupyter notebook notebooks/

# 4. Lanzar la app Streamlit
streamlit run app/Home.py
```

El dataset original (`data/raw/streaming_users_dirty.json`) debe estar presente para reproducir el pipeline desde cero. El dataset procesado (`data/processed/streaming_users_clean.csv`) se genera automáticamente al ejecutar el notebook 02.
# PI_Mineria_Datos_1
