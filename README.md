# Proyecto Integrador: Minería de Datos I

### Información General
- **Integrantes:** Santiago Gallardo y Valeria Martinetti
- **Materia:** Minería de Datos I
- **Aplicación Web:** [Ver en Streamlit Cloud](https://pi-mineria-datos-1.streamlit.app/)
- **Informe Final:** [Ver Informe en PDF](https://github.com/Vilemar130/PI_Mineria_Datos_1/tree/main/reportes)

### Objetivo del Proyecto
El propósito de este proyecto es analizar los patrones de consumo de los clientes de una plataforma de streaming, investigando si el tipo de plan de suscripción afecta el nivel de "engagement" (minutos visualizados) y el volumen de problemas técnicos reportados. Se busca realizar un análisis reproducible que vaya desde la limpieza de datos hasta el escalamiento y reducción dimensional, demostrando la capacidad de separar evidencia empírica de interpretaciones de negocio.

### Dataset
El dataset base, `streaming_users_dirty.json` (ubicado en `data/raw/`), contiene registros de clientes de Latinoamérica. Posee variables sociodemográficas (edad, país), preferencias (género favorito) y métricas de uso (minutos consumidos, plan contratado, tickets de soporte). Para la etapa de análisis se utiliza una versión procesada de este dataset disponible en [data/processed/streaming_users_clean.csv](data/processed/streaming_users_clean.csv).

### Estructura del Repositorio
- `data/`: Contiene el dataset crudo y el procesado.
- `notebooks/`: Desarrollo analítico en formato Jupyter.
- `app/`: Código fuente de la aplicación interactiva en Streamlit.
- `reports/`: Informe final.
- `logs/`: Registro de auditoría del proceso ETL.

### Preparación y Calidad de Datos
Todo el proceso de depuración está detallado en el notebook [02_calidad_y_limpieza.ipynb](notebooks/02_calidad_y_limpieza.ipynb). Se eliminaron duplicados absolutos y se descartaron registros con valores físicamente imposibles (tiempos negativos, edades fuera de rango o minutos que exceden la duración de un mes natural). Las fechas corruptas se filtraron tras el parseo, y los valores nulos numéricos se imputaron con la mediana estadística. Los géneros faltantes se catalogaron como "Otros". Todo este proceso fue auditado y su trazabilidad puede consultarse en [logs/pipeline_log.csv](logs/pipeline_log.csv). Retuvimos a 7265 usuarios, manteniendo intactos a los "Súper Usuarios" (outliers estadísticos).

### Resumen del Análisis Exploratorio
El análisis completo se encuentra en [03_eda.ipynb](notebooks/03_eda.ipynb). Mediante técnicas univariadas, se constató que la edad media es de 33 años y que el Plan Básico domina el mercado. En el análisis bivariado, los gráficos de densidad (violín) demostraron que el tiempo de uso mensual es idéntico entre usuarios de planes Básico, Estándar y Premium. Asimismo, la proporción de géneros favoritos se mantiene intacta sin importar la suscripción elegida. El cruce multivariado (País x Plan) confirmó que la estrategia comercial tiene un impacto simétrico en toda la región latinoamericana, revelando una base de usuarios extremadamente homogénea en sus hábitos de consumo.

### Reducción de Dimensionalidad
Desarrollado en [04_pca.ipynb](notebooks/04_pca.ipynb), el algoritmo PCA se aplicó sobre `age`, `monthly_watch_time_mins` y `customer_support_tickets`. Previo al modelado, los datos fueron estandarizados usando `StandardScaler` para evitar el dominio aritmético de los minutos sobre los tickets. El análisis de varianza explicada no mostró un "codo" claro, requiriendo 3 componentes para superar el 90%. Al proyectar los primeros dos componentes (Biplot), no se detectaron clústeres aislables según el plan de suscripción.

### Conclusiones
Profundizadas en [05_conclusiones.ipynb](notebooks/05_conclusiones.ipynb), la evidencia sugiere que el enganche con la plataforma es universal y no depende del nivel adquisitivo (plan). Las decisiones de retención no deberían segmentarse por plan de suscripción, ya que el uso base está estandarizado. Como limitación principal, carecemos de telemetría de hardware (ej. uso de Smart TV) y de un componente temporal para calcular el Churn Rate. Estas incorporaciones quedan propuestas como mejoras para iteraciones futuras.

### Visualización interactiva y Cómo Ejecutar Localmente
Para explorar interactivamente los hallazgos:
1. Clona este repositorio y navega a su directorio raíz.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta la aplicación de Streamlit: `streamlit run app/Home.py`
