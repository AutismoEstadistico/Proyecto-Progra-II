# Análisis Estadístico y Scouting Interactivo — EA Sports FC 26

Aplicación web interactiva desarrollada en **Python** utilizando **Shiny Express** para el curso de **Programación II**. El proyecto permite explorar, filtrar y analizar el rendimiento, atributos técnicos y distribución demográfica de los jugadores de la base de datos de **EAFC 26** mediante visualizaciones estadísticas personalizadas.

## Equipo de Desarrollo

* **Jose Miguel Villalobos**
* **Ian Guadamuz**
* **Armando Arauz**
* **Estefania Robles**

## Objetivos y Preguntas de Investigación

### Objetivo General

Desarrollar una herramienta de análisis exploratorio e interactivo que permita evaluar el nivel competitivo de las ligas, la especialización por posiciones, el impacto de la edad en el rendimiento y el talento específico en métricas clave dentro del ecosistema de EAFC 26.

### Preguntas de Investigación

A través de los cinco módulos visuales de la aplicación, el análisis responde a las siguientes interrogantes:

1. **Jerarquía Competitiva entre Ligas:** ¿Cuál es la liga estadísticamente más fuerte y consistente del mundo según la distribución de la valoración global (*Overall* / OVR) de sus plantillas, y cómo se comparan sus medianas y valores atípicos frente a otras competiciones?
2. **Especialización Táctica por Posición:** ¿Cómo varían las métricas promedio de rendimiento a lo largo de las distintas demarcaciones en el terreno de juego y qué perfiles estadísticos definen a cada línea táctica?
3. **Curva de Rendimiento y Edad:** ¿De qué manera se transforman los atributos técnicos y físicos promedio de los futbolistas al comparar dos cohortes generacionales o rangos de edad específicos definidos por el usuario?
4. **Élite del Disparo de Media y Larga Distancia:** ¿Quiénes son los 10 mejores especialistas en tiros lejanos (*Long Shots*) dentro de las ligas seleccionadas y cómo cambia este ranking al filtrar de forma combinada entre delanteros, mediocampistas y defensores?
5. **Demografía y Calidad bajo los Tres Palos:** ¿Cómo se distribuye la valoración global (*OVR*) de los porteros dentro de un rango de edad determinado y qué nacionalidades dominan proporcionalmente cada nivel de rendimiento?

## Visualizaciones y Funcionalidades Interactivas

La interfaz cuenta con controles dinámicos que actualizan los gráficos en tiempo real:

1. **Distribución de Overall por Liga (`Boxplot`):** Evalúa la dispersión, mediana y *outliers* del OVR por liga para determinar su fortaleza estadística.
2. **Perfil Promedio por Posición (`Líneas y Puntos`):** Muestra la evolución y contraste de las estadísticas promedio según la posición de los jugadores.
3. **Comparativa Generacional (`Gráfico de Radar / Spider`):** Contrasta simultáneamente los atributos promedio de todos los jugadores pertenecientes a dos rangos de edad configurables por el usuario.
4. **Top 10 Especialistas en Long Shots (`Gráfico de Barras`):** Filtra el Top 10 de jugadores con mejor tiro lejano permitiendo seleccionar múltiples ligas y combinar roles tácticos (delanteros, mediocampistas y/o defensores).
5. **Distribución de Porteros por OVR y Nacionalidad (`Histograma Apilado / Stacked`):** Visualiza la frecuencia de porteros según su OVR dentro de un rango de edad específico, desglosando la proporción que aporta cada país en cada barra.

## Arquitectura del Proyecto

El código está modularizado para separar la lógica de la interfaz, el procesamiento de datos y la identidad visual de las librerías gráficas:

```text
├── Proyecto EAFC26.py   # Aplicación principal desarrollada en Shiny Express
├── theme.py             # Tema visual personalizado para gráficos en plotnine (ggplot)
├── theme_sns.py         # Estilos y paletas personalizadas para Seaborn y Matplotlib
├── theme_ui.py          # Configuración de estilos, paleta y layout para la interfaz UI
└── data/                # Conjunto de datos de EAFC 26 (formato CSV)
```

## Stack Tecnológico

* **Framework Web:** `shiny` (Shiny Express para Python)
* **Manipulación y Análisis de Datos:** `pandas`, `numpy`
* **Visualización de Datos:**
  * `plotnine` (implementación de la gramática de gráficos de *ggplot2* en Python)
  * `seaborn`
  * `matplotlib`

## Instalación y Ejecución Local

Sigue estos pasos para ejecutar la aplicación en tu entorno local:

### 1. Clonar el repositorio

```bash
git clone <URL-DEL-REPOSITORIO>
cd <NOMBRE-DE-LA-CARPETA>
```

### 2. Crear y activar un entorno virtual (Recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

Asegúrate de tener instaladas las librerías necesarias:

```bash
pip install shiny pandas numpy matplotlib seaborn plotnine
```

### 4. Ejecutar la aplicación Shiny

Inicia el servidor local ejecutando el archivo principal (entre comillas debido al espacio en el nombre):

```bash
shiny run --reload "Proyecto EAFC26.py"
```

Una vez ejecutado, abre tu navegador en la dirección local que indica la terminal (generalmente `http://127.0.0.1:8000`).

## Flujo de Trabajo Colaborativo (Git)

El desarrollo se gestionó mediante un repositorio compartido aplicando buenas prácticas de control de versiones:

* Creación de ramas independientes (`feature/...`) para el desarrollo de cada visualización, temas personalizados y componentes de UI.
* Integración controlada hacia la rama principal (`main`) mediante *Pull Requests* y *merges* verificados.
* Commits atómicos y descriptivos documentando el progreso de cada integrante.